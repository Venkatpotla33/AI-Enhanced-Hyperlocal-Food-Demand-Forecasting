# ============================================================
# TRANSACTION-LEVEL FOOD ORDER GENERATION
# ============================================================

"""
Generate transaction-level synthetic food delivery orders
from the validated hourly zone-level demand signal.

Pipeline:

Hourly Realized Demand
        ↓
Integer Order Count
        ↓
Customer Selection
        ↓
Restaurant Selection
        ↓
Timestamp Generation
        ↓
Order Attributes
        ↓
Transaction-Level Orders
"""


# ============================================================
# IMPORTS
# ============================================================

from pathlib import Path
import sys

import numpy as np
import pandas as pd


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# IMPORT DEMAND GENERATION FUNCTIONS
# ============================================================

from src.data_generation.generate_demand import (
    create_hourly_timeline,
    apply_demand_patterns,
    apply_seasonal_variation,
    apply_behavioral_effects,
    add_surge_effect,
    add_stochastic_noise
)


# ============================================================
# PROJECT PATHS
# ============================================================

DATA_DIR = PROJECT_ROOT / "data"

RAW_ORDERS_DIR = DATA_DIR / "raw" / "orders"

RESTAURANT_FILE = (
    RAW_ORDERS_DIR / "restaurants.csv"
)

CUSTOMER_FILE = (
    RAW_ORDERS_DIR / "customers.csv"
)


# ============================================================
# RANDOM SEED
# ============================================================

RANDOM_SEED = 42

np.random.seed(RANDOM_SEED)


# ============================================================
# LOAD MASTER DATA
# ============================================================

def load_master_data():

    restaurants = pd.read_csv(
        RESTAURANT_FILE
    )

    customers = pd.read_csv(
        CUSTOMER_FILE
    )

    print("Master data loaded successfully!")

    print(
        f"Restaurants: {len(restaurants):,}"
    )

    print(
        f"Customers: {len(customers):,}"
    )

    return restaurants, customers


# ============================================================
# GENERATE HOURLY DEMAND
# ============================================================

def generate_hourly_demand(
    restaurants,
    customers
):
    """
    Generate the validated hourly zone-level
    synthetic demand signal.
    """

    # --------------------------------------------------------
    # CREATE HOURLY TIMELINE
    # --------------------------------------------------------

    demand_df = create_hourly_timeline()

    # --------------------------------------------------------
    # APPLY BASE DEMAND PATTERNS
    # --------------------------------------------------------

    demand_df = apply_demand_patterns(
        demand_df
    )

    # --------------------------------------------------------
    # APPLY SEASONAL VARIATION
    # --------------------------------------------------------

    demand_df = apply_seasonal_variation(
        demand_df
    )

    # --------------------------------------------------------
    # APPLY CUSTOMER + RESTAURANT EFFECTS
    # --------------------------------------------------------

    demand_df = apply_behavioral_effects(
        demand_df,
        restaurants,
        customers
    )

    # --------------------------------------------------------
    # APPLY CONTROLLED SURGE EFFECT
    # --------------------------------------------------------

    demand_df = add_surge_effect(
        demand_df
    )

    # --------------------------------------------------------
    # APPLY STOCHASTIC NOISE
    # --------------------------------------------------------

    demand_df = add_stochastic_noise(
        demand_df
    )

    print(
        "\nHourly demand generated successfully!"
    )

    print(
        f"Hourly-zone records: {len(demand_df):,}"
    )

    return demand_df


# ============================================================
# MAIN TEST
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # LOAD MASTER DATA
    # --------------------------------------------------------

    restaurants, customers = load_master_data()

    # --------------------------------------------------------
    # GENERATE HOURLY DEMAND
    # --------------------------------------------------------

    demand_df = generate_hourly_demand(
        restaurants,
        customers
    )

    # --------------------------------------------------------
    # DISPLAY SAMPLE
    # --------------------------------------------------------

    print(
        "\nFirst 5 hourly demand records:"
    )

    print(
        demand_df.head()
    )