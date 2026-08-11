import pandas as pd

from backend.recommender import apply_diet_filter


# ==================================================
# MEAL CALORIE DISTRIBUTION
# ==================================================

MEAL_PERCENTAGES = {
    "Breakfast": 0.25,
    "Lunch": 0.35,
    "Snack": 0.10,
    "Dinner": 0.30
}


# ==================================================
# CREATE MEAL
# ==================================================

def create_meal(
    food,
    target_calories
):
    """
    Create a meal from one food item.
    """

    calories_per_100g = food["Calories_per_100g"]

    if calories_per_100g <= 0:
        return None

    # Calculate serving size
    serving_g = (
        target_calories
        / calories_per_100g
    ) * 100

    # Keep serving size reasonable
    serving_g = max(
        50,
        min(serving_g, 500)
    )

    multiplier = serving_g / 100

    calories = (
        food["Calories_per_100g"]
        * multiplier
    )

    protein = (
        food["Protein_g"]
        * multiplier
    )

    carbs = (
        food["Carbs_g"]
        * multiplier
    )

    fat = (
        food["Fat_g"]
        * multiplier
    )

    return {
        "Food_Item": food["Food_Item"],
        "Serving_g": round(serving_g, 1),
        "Calories": round(calories, 1),
        "Protein_g": round(protein, 1),
        "Carbs_g": round(carbs, 1),
        "Fat_g": round(fat, 1)
    }


# ==================================================
# FIND BEST FOOD
# ==================================================

def find_best_food(
    foods,
    target_calories,
    target_protein=0,
    used_foods=None
):
    """
    Find the best food according to calories,
    protein and previous food usage.
    """

    if used_foods is None:
        used_foods = set()

    candidates = foods.copy()

    # Remove foods already used
    if used_foods:

        unused = candidates[
            ~candidates["Food_Item"].isin(
                used_foods
            )
        ]

        if not unused.empty:
            candidates = unused

    if candidates.empty:
        return None

    # Remove invalid calorie values
    candidates = candidates[
        candidates["Calories_per_100g"] > 0
    ].copy()

    if candidates.empty:
        return None

    # --------------------------------------------------
    # Calorie score
    # --------------------------------------------------

    candidates["calorie_score"] = abs(
        candidates["Calories_per_100g"]
        - target_calories
    )

    # --------------------------------------------------
    # Protein score
    # --------------------------------------------------

    if target_protein > 0:

        candidates["protein_score"] = abs(
            candidates["Protein_g"]
            - target_protein
        )

    else:

        candidates["protein_score"] = 0

    # --------------------------------------------------
    # Final score
    # --------------------------------------------------

    candidates["score"] = (
        candidates["calorie_score"] * 0.5
        +
        candidates["protein_score"] * 0.5
    )

    candidates = candidates.sort_values(
        "score"
    )

    return candidates.iloc[0]


# ==================================================
# DAILY MEAL PLAN
# ==================================================

def create_daily_meal_plan(
    df,
    calorie_target,
    diet_preference=None,
    used_foods=None
):
    """
    Create a complete daily meal plan.
    """

    if used_foods is None:
        used_foods = set()

    # Apply diet filter
    foods = apply_diet_filter(
        df,
        diet_preference
    )

    # Remove missing nutrition data
    foods = foods.dropna(
        subset=[
            "Food_Item",
            "Calories_per_100g",
            "Protein_g",
            "Fat_g",
            "Carbs_g"
        ]
    ).copy()

    if foods.empty:

        return {
            "Breakfast": None,
            "Lunch": None,
            "Snack": None,
            "Dinner": None
        }

    meal_plan = {}

    # Approximate protein distribution
    protein_distribution = {
        "Breakfast": 0.25,
        "Lunch": 0.35,
        "Snack": 0.10,
        "Dinner": 0.30
    }

    # --------------------------------------------------
    # Create each meal
    # --------------------------------------------------

    for meal_name, percentage in MEAL_PERCENTAGES.items():

        meal_calories = (
            calorie_target
            * percentage
        )

        meal_protein = (
            protein_distribution[meal_name]
            * 100
        )

        food = find_best_food(
            foods,
            meal_calories / 2,
            meal_protein,
            used_foods
        )

        if food is not None:

            meal = create_meal(
                food,
                meal_calories
            )

            meal_plan[meal_name] = meal

            used_foods.add(
                food["Food_Item"]
            )

        else:

            meal_plan[meal_name] = None

    return meal_plan


# ==================================================
# WEEKLY MEAL PLAN
# ==================================================

def create_weekly_meal_plan(
    df,
    calorie_target,
    diet_preference=None
):
    """
    Create a 7-day personalized meal plan.
    """

    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    weekly_plan = {}

    used_foods = set()

    # --------------------------------------------------
    # Generate each day
    # --------------------------------------------------

    for day in days:

        daily_plan = create_daily_meal_plan(
            df,
            calorie_target,
            diet_preference,
            used_foods
        )

        weekly_plan[day] = daily_plan

    return weekly_plan