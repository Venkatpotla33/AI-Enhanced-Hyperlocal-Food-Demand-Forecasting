"""
Generate synthetic customer master data for the
AI-Enhanced Hyperlocal Food Demand Forecasting project.

Phase 02 - Step 02.3
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
OUTPUT_FILE = OUTPUT_DIR / "customers.csv"


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
        "customer_share": 0.18,
    },
    {
        "zone_id": "Z02",
        "zone_name": "Hitech City",
        "customer_share": 0.24,
    },
    {
        "zone_id": "Z03",
        "zone_name": "Gachibowli",
        "customer_share": 0.22,
    },
    {
        "zone_id": "Z04",
        "zone_name": "Madhapur",
        "customer_share": 0.16,
    },
    {
        "zone_id": "Z05",
        "zone_name": "Kukatpally",
        "customer_share": 0.20,
    },
]


# ============================================================
# 4. CUSTOMER CONFIGURATION
# ============================================================

TOTAL_CUSTOMERS = 50_000


CUSTOMER_SEGMENTS = [
    "Occasional",
    "Regular",
    "Frequent",
]


CUSTOMER_SEGMENT_PROBABILITIES = [
    0.45,
    0.40,
    0.15,
]


# ============================================================
# 5. CUSTOMER SEGMENT ACTIVITY RANGES
# ============================================================

ACTIVITY_RANGES = {
    "Occasional": (0.05, 0.35),
    "Regular": (0.35, 0.70),
    "Frequent": (0.70, 1.00),
}


# ============================================================
# 6. PREFERRED ORDER VALUE RANGES
# ============================================================

ORDER_VALUE_RANGES = {
    "Occasional": (150, 350),
    "Regular": (180, 450),
    "Frequent": (220, 550),
}


# ============================================================
# 7. GENERATE CUSTOMER MASTER DATA
# ============================================================

def generate_customers() -> pd.DataFrame:
    """
    Generate synthetic customer master data.

    Returns
    -------
    pd.DataFrame
        Synthetic customer-level dataset.
    """

    customer_ids = [
        f"C{i:06d}"
        for i in range(1, TOTAL_CUSTOMERS + 1)
    ]

    # Assign home zones according to predefined shares.
    zone_indices = np.random.choice(
        len(ZONES),
        size=TOTAL_CUSTOMERS,
        p=[
            zone["customer_share"]
            for zone in ZONES
        ],
    )

    # Assign customer segments.
    segments = np.random.choice(
        CUSTOMER_SEGMENTS,
        size=TOTAL_CUSTOMERS,
        p=CUSTOMER_SEGMENT_PROBABILITIES,
    )

    records = []

    for customer_id, zone_index, segment in zip(
        customer_ids,
        zone_indices,
        segments,
    ):

        zone = ZONES[zone_index]

        activity_min, activity_max = ACTIVITY_RANGES[
            segment
        ]

        activity_score = round(
            np.random.uniform(
                activity_min,
                activity_max,
            ),
            3,
        )

        value_min, value_max = ORDER_VALUE_RANGES[
            segment
        ]

        preferred_order_value = round(
            np.random.uniform(
                value_min,
                value_max,
            ),
            2,
        )

        records.append(
            {
                "customer_id": customer_id,
                "home_zone_id": zone["zone_id"],
                "home_zone_name": zone["zone_name"],
                "customer_segment": segment,
                "customer_activity_score": activity_score,
                "preferred_order_value": preferred_order_value,
            }
        )

    return pd.DataFrame(records)


# ============================================================
# 8. VALIDATE CUSTOMER DATA
# ============================================================

def validate_customers(df: pd.DataFrame) -> None:
    """
    Validate the generated customer master dataset.
    """

    required_columns = [
        "customer_id",
        "home_zone_id",
        "home_zone_name",
        "customer_segment",
        "customer_activity_score",
        "preferred_order_value",
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

    # Check duplicate customer IDs
    if df["customer_id"].duplicated().any():
        raise ValueError(
            "Duplicate customer IDs detected."
        )

    # Check missing values
    if df[required_columns].isnull().any().any():
        raise ValueError(
            "Missing values detected in customer master data."
        )

    # Check activity score
    if not df["customer_activity_score"].between(
        0, 1
    ).all():
        raise ValueError(
            "Customer activity score must be between 0 and 1."
        )

    # Check preferred order value
    if (df["preferred_order_value"] <= 0).any():
        raise ValueError(
            "Preferred order value must be greater than zero."
        )


# ============================================================
# 9. SAVE CUSTOMER DATA
# ============================================================

def save_customers(df: pd.DataFrame) -> None:
    """
    Save customer master data as CSV.
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
# 10. MAIN
# ============================================================

def main():

    print("=" * 60)
    print("PHASE 02 - STEP 02.3")
    print("Synthetic Customer Master Data Generation")
    print("=" * 60)

    customers_df = generate_customers()

    validate_customers(customers_df)

    save_customers(customers_df)

    print()
    print("Customer generation completed successfully.")
    print()
    print(f"Total customers : {len(customers_df):,}")
    print(f"Output file     : {OUTPUT_FILE}")

    print()
    print("Customers by zone:")
    print(
        customers_df["home_zone_name"]
        .value_counts()
        .sort_index()
    )

    print()
    print("Customer segments:")
    print(
        customers_df["customer_segment"]
        .value_counts()
    )

    print()
    print("Sample records:")
    print(
        customers_df.head(10).to_string(
            index=False
        )
    )


if __name__ == "__main__":
    main()