import os
import pandas as pd


# ==================================================
# LOAD FITFUEL FOOD DATA
# ==================================================

def load_food_data():
    """
    Load the FitFuel healthy-food dataset.

    The CSV file must be located at:

        data/fitfuel_healthy_foods_flipkart.csv

    The Flipkart_Link column is preserved so that
    app.py can display Buy on Flipkart buttons.
    """

    # --------------------------------------------------
    # Find project root
    # --------------------------------------------------

    project_root = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    # --------------------------------------------------
    # New CSV path
    # --------------------------------------------------

    csv_path = os.path.join(
        project_root,
        "data",
        "fitfuel_healthy_foods_flipkart.csv"
    )

    # --------------------------------------------------
    # Check CSV exists
    # --------------------------------------------------

    if not os.path.exists(csv_path):

        raise FileNotFoundError(
            f"""
Food dataset not found.

Expected location:
{csv_path}

Please make sure the file:

fitfuel_healthy_foods_flipkart.csv

is inside the data folder.
"""
        )

    # --------------------------------------------------
    # Read CSV
    # --------------------------------------------------

    foods = pd.read_csv(csv_path)

    # --------------------------------------------------
    # Remove completely empty rows
    # --------------------------------------------------

    foods = foods.dropna(
        how="all"
    )

    # --------------------------------------------------
    # Clean column names
    # --------------------------------------------------

    foods.columns = (
        foods.columns
        .astype(str)
        .str.strip()
    )

    # --------------------------------------------------
    # Required columns
    # --------------------------------------------------

    required_columns = [
        "Food_Item",
        "Category",
        "Diet",
        "Calories_per_100g",
        "Protein_g",
        "Fat_g",
        "Carbs_g",
        "Flipkart_Link"
    ]

    # --------------------------------------------------
    # Check columns
    # --------------------------------------------------

    missing_columns = [
        column
        for column in required_columns
        if column not in foods.columns
    ]

    if missing_columns:

        raise ValueError(
            "The CSV is missing these required columns: "
            + ", ".join(missing_columns)
        )

    # --------------------------------------------------
    # Convert nutrition columns to numbers
    # --------------------------------------------------

    nutrition_columns = [
        "Calories_per_100g",
        "Protein_g",
        "Fat_g",
        "Carbs_g"
    ]

    for column in nutrition_columns:

        foods[column] = pd.to_numeric(
            foods[column],
            errors="coerce"
        )

    # --------------------------------------------------
    # Remove foods with invalid nutrition data
    # --------------------------------------------------

    foods = foods.dropna(
        subset=nutrition_columns
    )

    # --------------------------------------------------
    # Clean food names
    # --------------------------------------------------

    foods["Food_Item"] = (
        foods["Food_Item"]
        .astype(str)
        .str.strip()
    )

    # --------------------------------------------------
    # Clean category
    # --------------------------------------------------

    foods["Category"] = (
        foods["Category"]
        .astype(str)
        .str.strip()
    )

    # --------------------------------------------------
    # Clean diet
    # --------------------------------------------------

    foods["Diet"] = (
        foods["Diet"]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    # --------------------------------------------------
    # Clean Flipkart links
    # --------------------------------------------------

    foods["Flipkart_Link"] = (
        foods["Flipkart_Link"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # --------------------------------------------------
    # Remove duplicate foods
    # --------------------------------------------------

    foods = foods.drop_duplicates(
        subset=["Food_Item"]
    )

    # --------------------------------------------------
    # Reset index
    # --------------------------------------------------

    foods = foods.reset_index(
        drop=True
    )

    return foods
