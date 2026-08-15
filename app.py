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
# USER PROFILE STORAGE
# ==================================================

if "user_profile" not in st.session_state:
    st.session_state.user_profile = {}

if "user_name" not in st.session_state:
    st.session_state.user_name = ""


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    """
    <style>

    /* ==================================================
       MAIN BACKGROUND
       ================================================== */

    .stApp {
        background: linear-gradient(
            135deg,
            #f0fdf4 0%,
            #ffffff 50%,
            #ecfdf5 100%
        );
    }


    /* ==================================================
       MAIN TITLE
       ================================================== */

    .main-title {
        font-size: 48px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
        color: #15803d;
    }


    /* ==================================================
       SUBTITLE
       ================================================== */

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #166534;
        margin-bottom: 35px;
    }


    /* ==================================================
       SECTION TITLE
       ================================================== */

    .section-title {
        font-size: 28px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 15px;
        color: #166534;
    }


    /* ==================================================
       MEAL CARD
       ================================================== */

    .meal-card {
        background: white;
        padding: 22px;
        border-radius: 18px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        margin-bottom: 15px;
        min-height: 230px;
        border-top: 5px solid #16a34a;
    }


    /* ==================================================
       MEAL TITLE
       ================================================== */

    .meal-title {
        font-size: 22px;
        font-weight: 700;
        color: #166534;
        margin-bottom: 15px;
    }


    /* ==================================================
       FOOD NAME
       ================================================== */

    .food-name {
        font-size: 20px;
        font-weight: 700;
        color: #111827;
        margin-bottom: 15px;
    }


    /* ==================================================
       MEAL INFORMATION
       ================================================== */

    .meal-info {
        font-size: 15px;
        color: #374151;
        margin: 8px 0;
    }


    /* ==================================================
       SIDEBAR
       ================================================== */

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #f0fdf4,
            #ffffff
        );
    }


    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #166534;
    }


    /* ==================================================
       BUTTON
       ================================================== */

    .stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 48px;
        font-weight: 700;
        background-color: #16a34a;
        color: white;
        border: none;
    }


    .stButton > button:hover {
        background-color: #15803d;
        color: white;
    }


    /* ==================================================
       INPUTS
       ================================================== */

    input {
        border-radius: 10px !important;
    }


    div[data-baseweb="select"] > div {
        border-radius: 10px;
    }


    /* ==================================================
       METRIC CARDS
       ================================================== */

    div[data-testid="stMetric"] {
        background: white;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        border-top: 4px solid #16a34a;
    }


    /* ==================================================
       PROFILE CARD
       ================================================== */

    .profile-card {
        background: linear-gradient(
            135deg,
            #16a34a,
            #15803d
        );
        padding: 22px;
        border-radius: 18px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 5px 15px rgba(22, 163, 74, 0.20);
    }


    .profile-card h2 {
        margin: 0;
        color: white;
    }


    .profile-card p {
        margin-top: 8px;
        margin-bottom: 0;
        color: white;
    }


    /* ==================================================
       AUTHOR NAME
       ================================================== */

    .author-name {
        position: fixed;
        bottom: 8px;
        left: 50%;
        transform: translateX(-50%);
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

    st.header("👤 Enter Your Name & Information")


    # ==================================================
    # NAME
    # ==================================================

    name = st.text_input(
        "Your Name",
        value=st.session_state.user_name,
        placeholder="Enter your name"
    )


    # ==================================================
    # WEIGHT
    # ==================================================

    weight = st.number_input(
        "Weight (kg)",
        min_value=20.0,
        max_value=300.0,
        value=70.0,
        step=0.5
    )


    # ==================================================
    # HEIGHT
    # ==================================================

    height = st.number_input(
        "Height (cm)",
        min_value=100.0,
        max_value=250.0,
        value=175.0,
        step=1.0
    )


    # ==================================================
    # AGE
    # ==================================================

    age = st.number_input(
        "Age",
        min_value=10,
        max_value=100,
        value=20,
        step=1
    )


    # ==================================================
    # GENDER
    # ==================================================

    gender = st.selectbox(
        "Gender",
        [
            "male",
            "female"
        ]
    )


    # ==================================================
    # ACTIVITY
    # ==================================================

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


    # ==================================================
    # GOAL
    # ==================================================

    goal = st.selectbox(
        "Goal",
        [
            "weight_loss",
            "maintenance",
            "muscle_gain"
        ]
    )


    # ==================================================
    # DIET PREFERENCE
    # ==================================================

    diet_preference = st.selectbox(
        "Diet Preference",
        [
            "vegetarian",
            "vegan",
            "non_vegetarian"
        ]
    )


    st.divider()


    # ==================================================
    # GENERATE BUTTON
    # ==================================================

    calculate = st.button(
        "🚀 Generate My Plan",
        type="primary"
    )


# ==================================================
# MAIN APPLICATION
# ==================================================

if calculate:

    # ==================================================
    # CHECK NAME
    # ==================================================

    if not name.strip():

        st.warning(
            "⚠️ Please enter your name first."
        )

        st.stop()


    # ==================================================
    # STORE USER PROFILE
    # ==================================================

    st.session_state.user_name = name.strip()

    st.session_state.user_profile = {
        "name": name.strip(),
        "weight": weight,
        "height": height,
        "age": age,
        "gender": gender,
        "activity": activity,
        "goal": goal,
        "diet_preference": diet_preference
    }


    # ==================================================
    # SIMPLE PERSONALIZED HEADER
    # ==================================================

    st.success(
        f"👋 Hello, {st.session_state.user_name}!"
    )


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


    # ==================================================
    # SUCCESS MESSAGE
    # ==================================================

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
                # FLIPKART
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


    # ==================================================
    # DAILY MEAL CARDS
    # ==================================================

    if daily_plan:

        meal_columns = st.columns(4)


        for column, (meal_name, meal) in zip(
            meal_columns,
            daily_plan.items()
        ):

            with column:

                if meal is not None:

                    # ------------------------------------------
                    # MEAL TITLE
                    # ------------------------------------------

                    st.markdown(
                        f"## {meal_icons.get(meal_name, '🍽️')} "
                        f"{meal_name}"
                    )


                    # ------------------------------------------
                    # FOOD NAME
                    # ------------------------------------------

                    st.markdown(
                        f"### 🥗 {meal['Food_Item']}"
                    )


                    # ------------------------------------------
                    # SERVING
                    # ------------------------------------------

                    st.write(
                        f"🍽️ **Serving:** "
                        f"{meal['Serving_g']} g"
                    )


                    # ------------------------------------------
                    # CALORIES
                    # ------------------------------------------

                    st.write(
                        f"🔥 **Calories:** "
                        f"{meal['Calories']} kcal"
                    )


                    # ------------------------------------------
                    # PROTEIN
                    # ------------------------------------------

                    st.write(
                        f"💪 **Protein:** "
                        f"{meal['Protein_g']} g"
                    )


                    # ------------------------------------------
                    # CARBS
                    # ------------------------------------------

                    st.write(
                        f"🍚 **Carbs:** "
                        f"{meal['Carbs_g']} g"
                    )


                    # ------------------------------------------
                    # FAT
                    # ------------------------------------------

                    st.write(
                        f"🥑 **Fat:** "
                        f"{meal['Fat_g']} g"
                    )


                    # ------------------------------------------
                    # FLIPKART
                    # ------------------------------------------

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


    # ==================================================
    # WEEKLY PLAN
    # ==================================================

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
                            f"🥗 **{meal['Food_Item']}**"
                        )


                    with col2:

                        st.write(
                            f"🍽️ {meal['Serving_g']} g"
                        )


                    with col3:

                        st.write(
                            f"🔥 {meal['Calories']} kcal"
                        )


                    with col4:

                        st.write(
                            f"💪 {meal['Protein_g']} g protein"
                        )


                    with col5:

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
    # SAVED PROFILE
    # ==================================================

    st.markdown(
        '<div class="section-title">'
        '👤 Your Saved Profile'
        '</div>',
        unsafe_allow_html=True
    )


    profile_col1, profile_col2 = st.columns(2)


    with profile_col1:

        st.write(
            f"👤 **Name:** "
            f"{st.session_state.user_profile['name']}"
        )

        st.write(
            f"🎂 **Age:** "
            f"{st.session_state.user_profile['age']}"
        )

        st.write(
            f"⚧️ **Gender:** "
            f"{st.session_state.user_profile['gender']}"
        )

        st.write(
            f"⚖️ **Weight:** "
            f"{st.session_state.user_profile['weight']} kg"
        )


    with profile_col2:

        st.write(
            f"📏 **Height:** "
            f"{st.session_state.user_profile['height']} cm"
        )

        st.write(
            f"🏃 **Activity:** "
            f"{st.session_state.user_profile['activity']}"
        )

        st.write(
            f"🎯 **Goal:** "
            f"{st.session_state.user_profile['goal']}"
        )

        st.write(
            f"🥗 **Diet:** "
            f"{st.session_state.user_profile['diet_preference']}"
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


# ==================================================
# AUTHOR NAME
# ==================================================

st.markdown(
    """
    <div class="author-name">
        Abhirudra Mani Yadav
    </div>
    """,
    unsafe_allow_html=True
)
