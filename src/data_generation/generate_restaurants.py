"""
Generate synthetic restaurant master data for the
AI-Enhanced Hyperlocal Food Demand Forecasting project.

Phase 02 - Step 02.2
"""

from pathlib import Path
import random

import numpy as np
import pandas as pd


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = PROJECT_ROOT / "data" / "raw" / "orders"
OUTPUT_FILE = OUTPUT_DIR / "restaurants.csv"


# ============================================================
# 2. REPRODUCIBILITY
# ============================================================

RANDOM_SEED = 42

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)


# ============================================================
# 3. SYNTHETIC HYDERABAD ZONES
# ============================================================

ZONES = [
    {
        "zone_id": "Z01",
        "zone_name": "Kondapur",
        "zone_type": "IT_Residential",
        "demand_profile": "high",
        "restaurant_count": 40,
    },
    {
        "zone_id": "Z02",
        "zone_name": "Hitech City",
        "zone_type": "IT_Commercial",
        "demand_profile": "very_high",
        "restaurant_count": 50,
    },
    {
        "zone_id": "Z03",
        "zone_name": "Gachibowli",
        "zone_type": "IT_Residential",
        "demand_profile": "very_high",
        "restaurant_count": 45,
    },
    {
        "zone_id": "Z04",
        "zone_name": "Madhapur",
        "zone_type": "Commercial_Residential",
        "demand_profile": "high",
        "restaurant_count": 40,
    },
    {
        "zone_id": "Z05",
        "zone_name": "Kukatpally",
        "zone_type": "Residential_Commercial",
        "demand_profile": "high",
        "restaurant_count": 45,
    },
]


# ============================================================
# 4. RESTAURANT CATEGORIES
# ============================================================

RESTAURANT_CATEGORIES = [
    "Biryani",
    "South Indian",
    "North Indian",
    "Chinese",
    "Fast Food",
    "Pizza",
    "Burgers",
    "Desserts",
    "Cafe",
    "Healthy Food",
    "Bakery",
]


# ============================================================
# 5. CATEGORY PRICE RANGES
# ============================================================

CATEGORY_PRICE_RANGE = {
    "Biryani": (220, 550),
    "South Indian": (120, 350),
    "North Indian": (180, 450),
    "Chinese": (180, 450),
    "Fast Food": (150, 400),
    "Pizza": (250, 650),
    "Burgers": (180, 450),
    "Desserts": (120, 350),
    "Cafe": (150, 450),
    "Healthy Food": (200, 500),
    "Bakery": (100, 300),
}


# ============================================================
# 6. RESTAURANT NAME COMPONENTS
# ============================================================

RESTAURANT_PREFIXES = [
    "Hyderabad",
    "Urban",
    "Spice",
    "Royal",
    "City",
    "Fresh",
    "Food",
    "Taste",
    "Grand",
    "Daily",
    "Street",
    "Express",
    "Kitchen",
    "Flavours",
    "Home",
]

RESTAURANT_SUFFIXES = [
    "Kitchen",
    "House",
    "Hub",
    "Cafe",
    "Bites",
    "Restaurant",
    "Foods",
    "Corner",
    "Point",
    "Express",
    "Treats",
]


# ============================================================
# 7. GENERATE RESTAURANT NAME
# ============================================================

def generate_restaurant_name(index: int) -> str:
    """
    Generate a synthetic restaurant name.

    Parameters
    ----------
    index : int
        Restaurant sequence number.

    Returns
    -------
    str
        Synthetic restaurant name.
    """

    prefix = random.choice(RESTAURANT_PREFIXES)
    suffix = random.choice(RESTAURANT_SUFFIXES)

    return f"{prefix} {suffix} {index:03d}"


# ============================================================
# 8. GENERATE RESTAURANT MASTER DATA
# ============================================================

def generate_restaurants() -> pd.DataFrame:
    """
    Generate synthetic restaurant master data.

    Returns
    -------
    pd.DataFrame
        Restaurant-level synthetic dataset.
    """

    restaurants = []

    global_restaurant_number = 1

    for zone in ZONES:

        for _ in range(zone["restaurant_count"]):

            restaurant_id = (
                f"{zone['zone_id']}_R{global_restaurant_number:03d}"
            )

            restaurant_category = random.choice(
                RESTAURANT_CATEGORIES
            )

            min_price, max_price = CATEGORY_PRICE_RANGE[
                restaurant_category
            ]

            average_order_value = round(
                random.uniform(min_price, max_price),
                2,
            )

            base_popularity = round(
                np.random.beta(2.5, 2.0),
                3,
            )

            restaurants.append(
                {
                    "restaurant_id": restaurant_id,
                    "restaurant_name": generate_restaurant_name(
                        global_restaurant_number
                    ),
                    "zone_id": zone["zone_id"],
                    "zone_name": zone["zone_name"],
                    "zone_type": zone["zone_type"],
                    "restaurant_category": restaurant_category,
                    "base_popularity": base_popularity,
                    "average_order_value": average_order_value,
                }
            )

            global_restaurant_number += 1

    return pd.DataFrame(restaurants)


# ============================================================
# 9. VALIDATE RESTAURANT DATA
# ============================================================

def validate_restaurants(df: pd.DataFrame) -> None:
    """
    Validate the generated restaurant master dataset.
    """

    required_columns = [
        "restaurant_id",
        "restaurant_name",
        "zone_id",
        "zone_name",
        "zone_type",
        "restaurant_category",
        "base_popularity",
        "average_order_value",
    ]

    # Check required columns
    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    # Check duplicate restaurant IDs
    if df["restaurant_id"].duplicated().any():
        raise ValueError(
            "Duplicate restaurant IDs detected."
        )

    # Check missing values
    if df[required_columns].isnull().any().any():
        raise ValueError(
            "Missing values detected in restaurant master data."
        )

    # Check popularity range
    if not df["base_popularity"].between(0, 1).all():
        raise ValueError(
            "Restaurant popularity must be between 0 and 1."
        )

    # Check order values
    if (df["average_order_value"] <= 0).any():
        raise ValueError(
            "Average order value must be greater than zero."
        )


# ============================================================
# 10. SAVE DATASET
# ============================================================

def save_restaurants(df: pd.DataFrame) -> None:
    """
    Save restaurant master data as CSV.
    """

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False,
    )


# ============================================================
# 11. MAIN
# ============================================================

def main():

    print("=" * 60)
    print("PHASE 02 - STEP 02.2")
    print("Synthetic Restaurant Master Data Generation")
    print("=" * 60)

    restaurants_df = generate_restaurants()

    validate_restaurants(restaurants_df)

    save_restaurants(restaurants_df)

    print()
    print("Restaurant generation completed successfully.")
    print()
    print(f"Total restaurants : {len(restaurants_df):,}")
    print(
        f"Output file       : {OUTPUT_FILE}"
    )

    print()
    print("Restaurants by zone:")
    print(
        restaurants_df["zone_name"]
        .value_counts()
        .sort_index()
    )

    print()
    print("Restaurant categories:")
    print(
        restaurants_df["restaurant_category"]
        .value_counts()
    )

    print()
    print("Sample records:")
    print(
        restaurants_df.head(10).to_string(
            index=False
        )
    )


if __name__ == "__main__":
    main()