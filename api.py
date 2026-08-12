from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.calculations import create_nutrition_profile
from backend.data_processor import load_food_data
from backend.recommender import recommend_foods
from backend.meal_planner import (
    create_daily_meal_plan,
    create_weekly_meal_plan
)


# ==================================================
# CREATE FASTAPI APP
# ==================================================

app = FastAPI(
    title="FitFuel AI API",
    description="AI-powered Indian diet recommendation backend",
    version="1.0"
)


# ==================================================
# LOAD FOOD DATA
# ==================================================

try:
    foods = load_food_data()
    print("Food dataset loaded successfully!")
    print("Number of foods:", len(foods))

except Exception as e:
    foods = None
    print("Food dataset could not be loaded:")
    print(e)


# ==================================================
# USER PROFILE
# ==================================================

class UserProfile(BaseModel):

    weight: float
    height: float
    age: int
    gender: str
    activity: str
    goal: str
    diet_preference: str


# ==================================================
# HOME
# ==================================================

@app.get("/")
def home():

    return {
        "status": "success",
        "message": "FitFuel AI Backend is running!",
        "version": "1.0"
    }


# ==================================================
# HEALTH CHECK
# ==================================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# ==================================================
# NUTRITION PROFILE
# ==================================================

@app.post("/nutrition")
def nutrition(user: UserProfile):

    try:

        profile = create_nutrition_profile(
            user.weight,
            user.height,
            user.age,
            user.gender,
            user.activity,
            user.goal
        )

        return {
            "status": "success",
            "profile": profile
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ==================================================
# FOOD RECOMMENDATIONS
# ==================================================

@app.post("/recommendations")
def recommendations(user: UserProfile):

    if foods is None:

        raise HTTPException(
            status_code=500,
            detail="Food dataset could not be loaded."
        )

    try:

        profile = create_nutrition_profile(
            user.weight,
            user.height,
            user.age,
            user.gender,
            user.activity,
            user.goal
        )

        recommendations = recommend_foods(
            foods,
            profile["calorie_target"],
            profile["protein_g"],
            diet_preference=user.diet_preference,
            top_n=10
        )

        return {
            "status": "success",
            "recommendations": recommendations.to_dict(
                orient="records"
            )
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ==================================================
# DAILY MEAL PLAN
# ==================================================

@app.post("/daily-plan")
def daily_plan(user: UserProfile):

    if foods is None:

        raise HTTPException(
            status_code=500,
            detail="Food dataset could not be loaded."
        )

    try:

        profile = create_nutrition_profile(
            user.weight,
            user.height,
            user.age,
            user.gender,
            user.activity,
            user.goal
        )

        meal_plan = create_daily_meal_plan(
            foods,
            profile["calorie_target"],
            user.diet_preference
        )

        return {
            "status": "success",
            "daily_plan": meal_plan
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ==================================================
# 7-DAY MEAL PLAN
# ==================================================

@app.post("/weekly-plan")
def weekly_plan(user: UserProfile):

    if foods is None:

        raise HTTPException(
            status_code=500,
            detail="Food dataset could not be loaded."
        )

    try:

        profile = create_nutrition_profile(
            user.weight,
            user.height,
            user.age,
            user.gender,
            user.activity,
            user.goal
        )

        meal_plan = create_weekly_meal_plan(
            foods,
            profile["calorie_target"],
            user.diet_preference
        )

        return {
            "status": "success",
            "weekly_plan": meal_plan
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )