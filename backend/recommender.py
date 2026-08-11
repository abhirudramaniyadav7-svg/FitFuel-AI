import pandas as pd

from backend.ml_model import ml_recommend_foods


# ==================================================
# DIET FILTERING
# ==================================================

def apply_diet_filter(
    df,
    diet_preference=None
):
    """
    Filter foods according to diet preference.
    """

    foods = df.copy()

    if not diet_preference:
        return foods

    diet_preference = (
        diet_preference
        .lower()
        .strip()
    )

    non_vegetarian_words = [
        "chicken",
        "mutton",
        "fish",
        "prawn",
        "shrimp",
        "egg",
        "meat"
    ]

    animal_products = [
        "chicken",
        "mutton",
        "fish",
        "prawn",
        "shrimp",
        "egg",
        "meat",
        "milk",
        "paneer",
        "curd",
        "yogurt",
        "ghee",
        "butter"
    ]

    food_names = (
        foods["Food_Item"]
        .astype(str)
        .str.lower()
    )

    # --------------------------------------------------
    # Vegetarian
    # --------------------------------------------------

    if diet_preference == "vegetarian":

        pattern = "|".join(
            non_vegetarian_words
        )

        foods = foods[
            ~food_names.str.contains(
                pattern,
                na=False,
                regex=True
            )
        ]


    # --------------------------------------------------
    # Vegan
    # --------------------------------------------------

    elif diet_preference == "vegan":

        pattern = "|".join(
            animal_products
        )

        foods = foods[
            ~food_names.str.contains(
                pattern,
                na=False,
                regex=True
            )
        ]


    # --------------------------------------------------
    # Non-vegetarian
    # --------------------------------------------------

    elif diet_preference == "non_vegetarian":

        # Keep all foods
        foods = foods


    return foods.reset_index(
        drop=True
    )


# ==================================================
# NORMALIZE DIFFERENCE
# ==================================================

def calculate_difference(
    actual,
    target
):
    """
    Calculate normalized difference.

    A smaller value means the food is
    closer to the desired nutrition value.
    """

    target = max(
        float(target),
        1.0
    )

    difference = abs(
        float(actual) - float(target)
    )

    return difference / target


# ==================================================
# RECOMMEND FOODS
# ==================================================

def recommend_foods(
    df,
    calorie_target,
    protein_target,
    diet_preference=None,
    top_n=10
):
    """
    Combined AI food recommendation system.

    Uses:

    1. Diet filtering
    2. ML recommendation
    3. Calories
    4. Protein
    5. Carbohydrates
    6. Fat
    7. Combined nutrition score
    """

    foods = apply_diet_filter(
        df,
        diet_preference
    )


    # --------------------------------------------------
    # Check empty dataset
    # --------------------------------------------------

    if foods.empty:

        return pd.DataFrame(
            columns=df.columns
        )


    # --------------------------------------------------
    # Calculate approximate per-meal targets
    # --------------------------------------------------

    meal_calorie_target = (
        float(calorie_target) / 4
    )

    meal_protein_target = (
        float(protein_target) / 4
    )


    # --------------------------------------------------
    # ML Recommendation
    # --------------------------------------------------

    try:

        ml_results = ml_recommend_foods(
            foods,
            calorie_target,
            protein_target,
            top_n=min(
                max(top_n * 3, 15),
                len(foods)
            )
        )

    except Exception:

        # If ML model fails, use the
        # complete filtered dataset.
        ml_results = foods.copy()

        ml_results["ML_Distance"] = 0.0


    # --------------------------------------------------
    # Check ML results
    # --------------------------------------------------

    if ml_results.empty:

        return pd.DataFrame(
            columns=df.columns
        )


    ml_results = ml_results.copy()


    # --------------------------------------------------
    # Make sure nutrition columns are numeric
    # --------------------------------------------------

    nutrition_columns = [
        "Calories_per_100g",
        "Protein_g",
        "Carbs_g",
        "Fat_g"
    ]

    for column in nutrition_columns:

        if column in ml_results.columns:

            ml_results[column] = pd.to_numeric(
                ml_results[column],
                errors="coerce"
            )


    ml_results = ml_results.dropna(
        subset=[
            "Calories_per_100g",
            "Protein_g",
            "Carbs_g",
            "Fat_g"
        ]
    )


    if ml_results.empty:

        return pd.DataFrame(
            columns=df.columns
        )


    # ==================================================
    # NUTRITION DIFFERENCES
    # ==================================================

    # Calories
    ml_results["calorie_difference"] = (
        ml_results["Calories_per_100g"]
        .apply(
            lambda x:
            calculate_difference(
                x,
                meal_calorie_target
            )
        )
    )


    # Protein
    ml_results["protein_difference"] = (
        ml_results["Protein_g"]
        .apply(
            lambda x:
            calculate_difference(
                x,
                meal_protein_target
            )
        )
    )


    # ==================================================
    # CARBS DIFFERENCE
    # ==================================================

    # Estimate carbohydrates target
    # from remaining calories.

    carbs_target = (
        float(calorie_target) * 0.45
    ) / 4 / 4


    ml_results["carbs_difference"] = (
        ml_results["Carbs_g"]
        .apply(
            lambda x:
            calculate_difference(
                x,
                carbs_target
            )
        )
    )


    # ==================================================
    # FAT DIFFERENCE
    # ==================================================

    # Estimate fat target.

    fat_target = (
        float(calorie_target) * 0.25
    ) / 9 / 4


    ml_results["fat_difference"] = (
        ml_results["Fat_g"]
        .apply(
            lambda x:
            calculate_difference(
                x,
                fat_target
            )
        )
    )


    # ==================================================
    # ML DISTANCE
    # ==================================================

    if "ML_Distance" not in ml_results.columns:

        ml_results["ML_Distance"] = 0.0

    else:

        ml_results["ML_Distance"] = pd.to_numeric(
            ml_results["ML_Distance"],
            errors="coerce"
        ).fillna(0)


    # Normalize ML distance.

    max_ml_distance = (
        ml_results["ML_Distance"].max()
    )

    if max_ml_distance > 0:

        ml_results["normalized_ml_distance"] = (
            ml_results["ML_Distance"]
            / max_ml_distance
        )

    else:

        ml_results["normalized_ml_distance"] = 0.0


    # ==================================================
    # FINAL RECOMMENDATION SCORE
    # ==================================================

    ml_results["recommendation_score"] = (

        # Machine-learning similarity
        ml_results["normalized_ml_distance"] * 0.35

        +

        # Calories
        ml_results["calorie_difference"] * 0.25

        +

        # Protein
        ml_results["protein_difference"] * 0.25

        +

        # Carbohydrates
        ml_results["carbs_difference"] * 0.075

        +

        # Fat
        ml_results["fat_difference"] * 0.075
    )


    # ==================================================
    # SORT RECOMMENDATIONS
    # ==================================================

    recommendations = (
        ml_results
        .sort_values(
            "recommendation_score",
            ascending=True
        )
        .head(top_n)
        .reset_index(drop=True)
    )


    return recommendations


# ==================================================
# HIGH PROTEIN FOODS
# ==================================================

def get_high_protein_foods(
    df,
    diet_preference=None,
    top_n=10
):
    """
    Return foods with the highest protein.
    """

    foods = apply_diet_filter(
        df,
        diet_preference
    )


    foods = foods.sort_values(
        "Protein_g",
        ascending=False
    )


    return foods.head(
        top_n
    ).reset_index(
        drop=True
    )


# ==================================================
# LOW CALORIE FOODS
# ==================================================

def get_low_calorie_foods(
    df,
    diet_preference=None,
    top_n=10
):
    """
    Return foods with the lowest calories.
    """

    foods = apply_diet_filter(
        df,
        diet_preference
    )


    foods = foods.sort_values(
        "Calories_per_100g",
        ascending=True
    )


    return foods.head(
        top_n
    ).reset_index(
        drop=True
    )
