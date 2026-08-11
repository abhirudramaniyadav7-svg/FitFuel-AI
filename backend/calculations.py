def calculate_bmi(weight_kg, height_cm):
    """
    Calculate BMI from weight and height.
    """

    if weight_kg <= 0:
        raise ValueError("Weight must be greater than 0.")

    if height_cm <= 0:
        raise ValueError("Height must be greater than 0.")

    height_m = height_cm / 100

    bmi = weight_kg / (height_m ** 2)

    return round(bmi, 2)


def get_bmi_category(bmi):
    """
    Return BMI category.
    """

    if bmi < 18.5:
        return "Underweight"

    elif bmi < 25:
        return "Normal"

    elif bmi < 30:
        return "Overweight"

    else:
        return "Obese"


def calculate_bmr(
    weight_kg,
    height_cm,
    age,
    gender
):
    """
    Calculate Basal Metabolic Rate using
    the Mifflin-St Jeor equation.
    """

    if gender.lower() == "male":

        bmr = (
            10 * weight_kg
            + 6.25 * height_cm
            - 5 * age
            + 5
        )

    else:

        bmr = (
            10 * weight_kg
            + 6.25 * height_cm
            - 5 * age
            - 161
        )

    return round(bmr, 2)


def calculate_tdee(bmr, activity):
    """
    Calculate Total Daily Energy Expenditure.
    """

    activity_multipliers = {

        "sedentary": 1.2,

        "light": 1.375,

        "moderate": 1.55,

        "active": 1.725,

        "very_active": 1.9
    }

    multiplier = activity_multipliers.get(
        activity.lower(),
        1.2
    )

    tdee = bmr * multiplier

    return round(tdee, 2)


def calculate_calorie_target(
    tdee,
    goal
):
    """
    Calculate daily calorie target based on goal.
    """

    goal = goal.lower()

    if goal == "weight_loss":

        calories = tdee - 500

    elif goal == "muscle_gain":

        calories = tdee + 300

    else:

        calories = tdee

    return round(calories, 2)


def calculate_macros(
    calorie_target,
    weight_kg,
    goal
):
    """
    Calculate daily protein, carbohydrate
    and fat targets.
    """

    # Protein target
    if goal.lower() == "muscle_gain":

        protein_g = weight_kg * 2.0

    elif goal.lower() == "weight_loss":

        protein_g = weight_kg * 1.8

    else:

        protein_g = weight_kg * 1.6


    # Fat = approximately 25% of calories
    fat_calories = calorie_target * 0.25

    fat_g = fat_calories / 9


    # Remaining calories come from carbohydrates
    protein_calories = protein_g * 4
    remaining_calories = (
        calorie_target
        - protein_calories
        - fat_calories
    )

    carbs_g = remaining_calories / 4

    return {
        "protein_g": round(protein_g, 2),
        "carbs_g": round(max(carbs_g, 0), 2),
        "fat_g": round(fat_g, 2)
    }


def create_nutrition_profile(
    weight,
    height,
    age,
    gender,
    activity,
    goal
):
    """
    Create complete nutrition profile.
    """

    bmi = calculate_bmi(
        weight,
        height
    )

    bmi_category = get_bmi_category(
        bmi
    )

    bmr = calculate_bmr(
        weight,
        height,
        age,
        gender
    )

    tdee = calculate_tdee(
        bmr,
        activity
    )

    calorie_target = calculate_calorie_target(
        tdee,
        goal
    )

    macros = calculate_macros(
        calorie_target,
        weight,
        goal
    )

    return {
        "bmi": bmi,
        "bmi_category": bmi_category,
        "bmr": bmr,
        "tdee": tdee,
        "calorie_target": calorie_target,
        "protein_g": macros["protein_g"],
        "carbs_g": macros["carbs_g"],
        "fat_g": macros["fat_g"]
    }