import pandas as pd
import streamlit as st

from backend.calculations import create_nutrition_profile
from backend.data_processor import load_food_data
from backend.recommender import recommend_foods
from backend.meal_planner import (
    create_daily_meal_plan,
    create_weekly_meal_plan
)


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="FitFuel AI",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f5f7f9;
    }

    .main-title {
        font-size: 48px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #666666;
        margin-bottom: 35px;
    }

    .section-title {
        font-size: 28px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    .meal-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        margin-bottom: 15px;
        min-height: 220px;
    }

    .meal-title {
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    section[data-testid="stSidebar"] {
        background-color: white;
    }

    .stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 45px;
        font-weight: 700;
    }

    /* ==================================================
       AUTHOR NAME - BOTTOM RIGHT
       ================================================== */

    .author-name {
        position: fixed;
        right: 15px;
        bottom: 10px;
        font-size: 12px;
        font-weight: 500;
        color: #555555;
        opacity: 0.70;
        z-index: 999999;
        pointer-events: none;
        white-space: nowrap;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# LOAD FOOD DATA
# ==================================================

try:

    foods = load_food_data()

except Exception as e:

    st.error(
        f"Unable to load food dataset: {e}"
    )

    st.stop()


# ==================================================
# HEADER
# ==================================================

st.markdown(
    '<div class="main-title">🥗 FitFuel AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Personalized Indian Diet & Nutrition Recommendation System'
    '</div>',
    unsafe_allow_html=True
)


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.header("👤 Your Profile")

    weight = st.number_input(
        "Weight (kg)",
        min_value=20.0,
        max_value=300.0,
        value=70.0,
        step=0.5
    )

    height = st.number_input(
        "Height (cm)",
        min_value=100.0,
        max_value=250.0,
        value=175.0,
        step=1.0
    )

    age = st.number_input(
        "Age",
        min_value=10,
        max_value=100,
        value=20,
        step=1
    )

    gender = st.selectbox(
        "Gender",
        [
            "male",
            "female"
        ]
    )

    activity = st.selectbox(
        "Activity Level",
        [
            "sedentary",
            "light",
            "moderate",
            "active",
            "very_active"
        ]
    )

    goal = st.selectbox(
        "Goal",
        [
            "weight_loss",
            "maintenance",
            "muscle_gain"
        ]
    )

    diet_preference = st.selectbox(
        "Diet Preference",
        [
            "vegetarian",
            "vegan",
            "non_vegetarian"
        ]
    )

    st.divider()

    calculate = st.button(
        "🚀 Generate My Plan",
        type="primary"
    )


# ==================================================
# MAIN APPLICATION
# ==================================================

if calculate:

    # ==================================================
    # NUTRITION PROFILE
    # ==================================================

    try:

        profile = create_nutrition_profile(
            weight,
            height,
            age,
            gender,
            activity,
            goal
        )

    except Exception as e:

        st.error(
            f"Nutrition calculation error: {e}"
        )

        st.stop()


    st.success(
        "🎉 Your personalized FitFuel plan has been generated!"
    )


    # ==================================================
    # NUTRITION DASHBOARD
    # ==================================================

    st.markdown(
        '<div class="section-title">'
        '📊 Your Nutrition Dashboard'
        '</div>',
        unsafe_allow_html=True
    )


    # ==================================================
    # METRICS
    # ==================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "BMI",
            profile["bmi"]
        )

        st.caption(
            f"Category: {profile['bmi_category']}"
        )


    with col2:

        st.metric(
            "BMR",
            f'{profile["bmr"]} kcal'
        )


    with col3:

        st.metric(
            "TDEE",
            f'{profile["tdee"]} kcal'
        )


    with col4:

        st.metric(
            "Daily Calories",
            f'{profile["calorie_target"]} kcal'
        )


    # ==================================================
    # MACRONUTRIENTS
    # ==================================================

    st.markdown(
        '<div class="section-title">'
        '🥩 Daily Macronutrient Targets'
        '</div>',
        unsafe_allow_html=True
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "🥩 Protein",
            f'{profile["protein_g"]} g'
        )


    with col2:

        st.metric(
            "🍚 Carbohydrates",
            f'{profile["carbs_g"]} g'
        )


    with col3:

        st.metric(
            "🥑 Fat",
            f'{profile["fat_g"]} g'
        )


    # ==================================================
    # AI FOOD RECOMMENDATIONS
    # ==================================================

    st.markdown(
        '<div class="section-title">'
        '🤖 AI Recommended Indian Foods'
        '</div>',
        unsafe_allow_html=True
    )


    st.write(
        "FitFuel AI analyzes your nutrition requirements "
        "and recommends foods that match your calorie "
        "and protein targets."
    )


    try:

        recommendations = recommend_foods(
            foods,
            profile["calorie_target"],
            profile["protein_g"],
            diet_preference=diet_preference,
            top_n=10
        )

    except Exception as e:

        st.error(
            f"Recommendation engine error: {e}"
        )

        recommendations = None


    # ==================================================
    # RECOMMENDATION RESULTS
    # ==================================================

    if recommendations is not None:

        if recommendations.empty:

            st.warning(
                "No suitable foods were found "
                "for your preferences."
            )

        else:

            for _, food in recommendations.iterrows():

                col1, col2, col3 = st.columns(
                    [4, 2, 1]
                )


                # ------------------------------------------
                # FOOD NAME
                # ------------------------------------------

                with col1:

                    st.markdown(
                        f"### 🥗 {food['Food_Item']}"
                    )

                    st.write(
                        f"**Category:** "
                        f"{food['Category']}"
                    )

                    if "Diet" in food.index:

                        st.write(
                            f"**Diet:** "
                            f"{str(food['Diet']).replace('_', ' ').title()}"
                        )


                # ------------------------------------------
                # NUTRITION
                # ------------------------------------------

                with col2:

                    st.write(
                        f"🔥 **{food['Calories_per_100g']} kcal**"
                    )

                    st.write(
                        f"💪 **{food['Protein_g']} g protein**"
                    )

                    st.write(
                        f"🥑 **{food['Fat_g']} g fat**"
                    )

                    st.write(
                        f"🍚 **{food['Carbs_g']} g carbs**"
                    )


                # ------------------------------------------
                # FLIPKART BUTTON
                # ------------------------------------------

                with col3:

                    flipkart_link = ""

                    if "Flipkart_Link" in food.index:

                        flipkart_link = food["Flipkart_Link"]


                    if (
                        pd.notna(flipkart_link)
                        and str(flipkart_link).strip() != ""
                    ):

                        st.link_button(
                            "🛒 Buy on Flipkart",
                            str(flipkart_link)
                        )

                    else:

                        st.caption(
                            "No shopping link available"
                        )


                st.divider()


    # ==================================================
    # DAILY MEAL PLAN
    # ==================================================

    st.markdown(
        '<div class="section-title">'
        "🍽️ Today's Meal Plan"
        '</div>',
        unsafe_allow_html=True
    )


    try:

        daily_plan = create_daily_meal_plan(
            foods,
            profile["calorie_target"],
            diet_preference
        )

    except Exception as e:

        st.error(
            f"Daily meal planner error: {e}"
        )

        daily_plan = {}


    meal_icons = {
        "Breakfast": "🥣",
        "Lunch": "🍛",
        "Snack": "🍎",
        "Dinner": "🍽️"
    }


    if daily_plan:

        meal_columns = st.columns(4)


        for column, (meal_name, meal) in zip(
            meal_columns,
            daily_plan.items()
        ):

            with column:

                if meal is not None:

                    st.markdown(
                        f"""
                        <div class="meal-card">

                        <div class="meal-title">
                        {meal_icons.get(
                            meal_name,
                            "🍽️"
                        )}
                        {meal_name}
                        </div>

                        <b>{meal["Food_Item"]}</b>

                        <br><br>

                        <b>Serving:</b>
                        {meal["Serving_g"]} g

                        <br>

                        <b>Calories:</b>
                        {meal["Calories"]} kcal

                        <br>

                        <b>Protein:</b>
                        {meal["Protein_g"]} g

                        <br>

                        <b>Carbs:</b>
                        {meal["Carbs_g"]} g

                        <br>

                        <b>Fat:</b>
                        {meal["Fat_g"]} g

                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                    # Flipkart link for meal

                    if "Flipkart_Link" in meal:

                        meal_link = meal["Flipkart_Link"]


                        if (
                            pd.notna(meal_link)
                            and str(meal_link).strip() != ""
                        ):

                            st.link_button(
                                "🛒 Buy on Flipkart",
                                str(meal_link)
                            )

                else:

                    st.warning(
                        f"No food found for {meal_name}."
                    )


    # ==================================================
    # 7-DAY MEAL PLAN
    # ==================================================

    st.markdown(
        '<div class="section-title">'
        '📅 Your 7-Day Meal Plan'
        '</div>',
        unsafe_allow_html=True
    )


    try:

        weekly_plan = create_weekly_meal_plan(
            foods,
            profile["calorie_target"],
            diet_preference
        )

    except Exception as e:

        st.error(
            f"Weekly meal planner error: {e}"
        )

        weekly_plan = {}


    for day, daily_plan in weekly_plan.items():

        with st.expander(
            f"📅 {day}"
        ):

            for meal_name, meal in daily_plan.items():

                if meal is not None:

                    st.markdown(
                        f"### "
                        f"{meal_icons.get(meal_name, '🍽️')} "
                        f"{meal_name}"
                    )


                    col1, col2, col3, col4, col5 = st.columns(
                        [3, 1.5, 1.5, 1.5, 1.5]
                    )


                    with col1:

                        st.write(
                            f"**{meal['Food_Item']}**"
                        )


                    with col2:

                        st.write(
                            f"{meal['Serving_g']} g"
                        )


                    with col3:

                        st.write(
                            f"{meal['Calories']} kcal"
                        )


                    with col4:

                        st.write(
                            f"{meal['Protein_g']} g protein"
                        )


                    with col5:

                        # ----------------------------------
                        # WEEKLY MEAL FLIPKART LINK
                        # ----------------------------------

                        meal_link = ""

                        if "Flipkart_Link" in meal:

                            meal_link = meal["Flipkart_Link"]


                        if (
                            pd.notna(meal_link)
                            and str(meal_link).strip() != ""
                        ):

                            st.link_button(
                                "🛒 Buy",
                                str(meal_link)
                            )


                else:

                    st.warning(
                        f"No suitable food found "
                        f"for {meal_name}."
                    )


    # ==================================================
    # FOOTER
    # ==================================================

    st.divider()

    st.caption(
        "FitFuel AI • Nutrition calculations • "
        "Food data processing • ML recommendation "
        "engine • Personalized meal planning"
    )

    st.caption(
        "🛒 Product links open Flipkart search results. "
        "Prices and availability are controlled by Flipkart."
    )


else:

    # ==================================================
    # WELCOME SCREEN
    # ==================================================

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:60px 20px;
        ">

        <h2>🥗 Welcome to FitFuel AI</h2>

        <p style="font-size:18px;">
        Your personalized Indian nutrition
        recommendation system.
        </p>

        <p>
        Enter your information in the sidebar
        and click <b>Generate My Plan</b>.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# ==================================================
# AUTHOR NAME
# ALWAYS VISIBLE - BOTTOM RIGHT
# ==================================================

st.markdown(
    """
    <div class="author-name">
        Abhirudra Mani Yadav
    </div>
    """,
    unsafe_allow_html=True
)
