import pandas as pd


# ==================================================
# REQUIRED DATASET COLUMNS
# ==================================================

REQUIRED_COLUMNS = [
    "Food_Item",
    "Category",
    "Calories_per_100g",
    "Protein_g",
    "Fat_g",
    "Carbs_g"
]


# ==================================================
# LOAD FOOD DATA
# ==================================================

def load_food_data():
    """
    Load and clean the Indian food nutrition dataset.
    """

    file_path = "data/indian_food_nutrition.csv"

    try:

        df = pd.read_csv(file_path)

    except FileNotFoundError:

        raise FileNotFoundError(
            "Indian food dataset not found. "
            "Make sure the file is located at "
            "'data/indian_food_nutrition.csv'."
        )


    # --------------------------------------------------
    # Check required columns
    # --------------------------------------------------

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            f"Missing columns in dataset: "
            f"{missing_columns}"
        )


    # --------------------------------------------------
    # Remove completely empty rows
    # --------------------------------------------------

    df = df.dropna(
        how="all"
    )


    # --------------------------------------------------
    # Convert nutrition columns to numeric
    # --------------------------------------------------

    numeric_columns = [
        "Calories_per_100g",
        "Protein_g",
        "Fat_g",
        "Carbs_g"
    ]

    for column in numeric_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


    # --------------------------------------------------
    # Remove rows with missing important values
    # --------------------------------------------------

    df = df.dropna(
        subset=[
            "Food_Item",
            "Calories_per_100g",
            "Protein_g",
            "Fat_g",
            "Carbs_g"
        ]
    )


    # --------------------------------------------------
    # Remove impossible nutrition values
    # --------------------------------------------------

    df = df[
        (df["Calories_per_100g"] >= 0)
        & (df["Protein_g"] >= 0)
        & (df["Fat_g"] >= 0)
        & (df["Carbs_g"] >= 0)
    ]


    # --------------------------------------------------
    # Clean food names
    # --------------------------------------------------

    df["Food_Item"] = (
        df["Food_Item"]
        .astype(str)
        .str.strip()
    )


    # --------------------------------------------------
    # Clean category
    # --------------------------------------------------

    df["Category"] = (
        df["Category"]
        .astype(str)
        .str.strip()
    )


    # --------------------------------------------------
    # Remove duplicate foods
    # --------------------------------------------------

    df = df.drop_duplicates(
        subset=["Food_Item"]
    )


    # --------------------------------------------------
    # Reset index
    # --------------------------------------------------

    df = df.reset_index(
        drop=True
    )


    return df


# ==================================================
# FILTER BY CATEGORY
# ==================================================

def filter_foods_by_category(
    df,
    category
):
    """
    Filter foods according to category.
    """

    if not category:
        return df.copy()

    filtered_df = df[
        df["Category"]
        .astype(str)
        .str.lower()
        .str.strip()
        == category.lower().strip()
    ]

    return filtered_df


# ==================================================
# GET DATASET SUMMARY
# ==================================================

def get_food_data_summary(df):
    """
    Return useful information about the food dataset.
    """

    return {
        "total_foods": len(df),
        "categories": df["Category"].nunique(),
        "average_calories": round(
            df["Calories_per_100g"].mean(),
            2
        ),
        "average_protein": round(
            df["Protein_g"].mean(),
            2
        ),
        "average_fat": round(
            df["Fat_g"].mean(),
            2
        ),
        "average_carbs": round(
            df["Carbs_g"].mean(),
            2
        )
    }