import numpy as np

from sklearn.neighbors import NearestNeighbors


# ==================================================
# FEATURE COLUMNS
# ==================================================

FEATURE_COLUMNS = [
    "Calories_per_100g",
    "Protein_g",
    "Fat_g",
    "Carbs_g"
]


# ==================================================
# TRAIN RECOMMENDATION MODEL
# ==================================================

def train_recommendation_model(df):
    """
    Train a KNN recommendation model
    using food nutrition data.
    """

    data = df[
        FEATURE_COLUMNS
    ].copy()

    # Remove missing values
    data = data.dropna()

    if data.empty:
        raise ValueError(
            "No valid nutrition data available."
        )

    # Number of neighbors
    n_neighbors = min(
        10,
        len(data)
    )

    # Create KNN model
    model = NearestNeighbors(
        n_neighbors=n_neighbors,
        metric="euclidean"
    )

    # Train model
    model.fit(data)

    return model, data.index


# ==================================================
# ML FOOD RECOMMENDATION
# ==================================================

def ml_recommend_foods(
    df,
    calorie_target,
    protein_target,
    top_n=10
):
    """
    Recommend foods using K-Nearest Neighbors.
    """

    if df.empty:
        return df.copy()

    # Keep required columns
    clean_df = df.dropna(
        subset=FEATURE_COLUMNS
    ).copy()

    if clean_df.empty:
        return clean_df

    # Train model
    model, _ = train_recommendation_model(
        clean_df
    )

    # --------------------------------------------------
    # Target nutrition profile
    # --------------------------------------------------

    target_calories = calorie_target / 4

    target_protein = protein_target / 4

    # Approximate meal-level targets
    target_fat = 25

    target_carbs = 50

    target = np.array([
        [
            target_calories,
            target_protein,
            target_fat,
            target_carbs
        ]
    ])

    # --------------------------------------------------
    # Number of recommendations
    # --------------------------------------------------

    number = min(
        top_n,
        len(clean_df)
    )

    # --------------------------------------------------
    # Find nearest foods
    # --------------------------------------------------

    distances, positions = model.kneighbors(
        target,
        n_neighbors=number
    )

    # --------------------------------------------------
    # Select foods
    # --------------------------------------------------

    recommendations = clean_df.iloc[
        positions[0]
    ].copy()

    # Add ML distance
    recommendations["ML_Distance"] = (
        distances[0]
    )

    # Smaller distance = better match
    recommendations = recommendations.sort_values(
        "ML_Distance"
    )

    return recommendations.reset_index(
        drop=True
    )