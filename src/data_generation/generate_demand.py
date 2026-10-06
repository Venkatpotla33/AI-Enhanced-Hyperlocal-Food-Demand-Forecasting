"""
Synthetic Demand Generation
Phase 02.4.1 - Demand Parameters

This module defines the parameters used to simulate
realistic hourly food demand across Hyderabad zones.
"""

# ============================================================
# PROJECT CONFIGURATION
# ============================================================

CITY = "Hyderabad"
START_DATE = "2023-01-01"
END_DATE = "2026-08-31"


# ============================================================
# ZONE BASE DEMAND
# ============================================================

ZONE_BASE_DEMAND = {
    "Z01": 100,   # Kondapur
    "Z02": 125,   # Hitech City
    "Z03": 120,   # Gachibowli
    "Z04": 105,   # Madhapur
    "Z05": 110    # Kukatpally
}


# ============================================================
# ZONE DEMAND MULTIPLIERS
# ============================================================

ZONE_MULTIPLIERS = {
    "Z01": 1.00,  # Kondapur
    "Z02": 1.25,  # Hitech City
    "Z03": 1.20,  # Gachibowli
    "Z04": 1.10,  # Madhapur
    "Z05": 1.08   # Kukatpally
}


# ============================================================
# WEEKLY DEMAND MULTIPLIERS
# ============================================================

DAY_MULTIPLIERS = {
    0: 0.90,   # Monday
    1: 0.95,   # Tuesday
    2: 1.00,   # Wednesday
    3: 1.05,   # Thursday
    4: 1.15,   # Friday
    5: 1.25,   # Saturday
    6: 1.10    # Sunday
}


# ============================================================
# HOURLY DEMAND MULTIPLIERS
# ============================================================

HOUR_MULTIPLIERS = {
    0: 0.20,
    1: 0.18,
    2: 0.16,
    3: 0.15,
    4: 0.15,
    5: 0.18,

    6: 0.25,
    7: 0.45,
    8: 0.65,
    9: 0.75,

    10: 0.55,
    11: 0.90,

    12: 1.35,
    13: 1.60,
    14: 1.40,

    15: 0.75,
    16: 0.60,
    17: 0.70,

    18: 1.10,
    19: 1.35,
    20: 1.55,
    21: 1.80,
    22: 1.45,

    23: 0.85
}


# ============================================================
# SEASONAL MULTIPLIERS
# ============================================================

MONTH_MULTIPLIERS = {
    1: 0.95,   # January
    2: 0.98,   # February
    3: 1.00,   # March
    4: 0.96,   # April
    5: 0.92,   # May
    6: 0.98,   # June
    7: 1.00,   # July
    8: 1.02,   # August
    9: 1.05,   # September
    10: 1.08,  # October
    11: 1.12,  # November
    12: 1.15   # December
}


# ============================================================
# CUSTOMER SEGMENT MULTIPLIERS
# ============================================================

CUSTOMER_SEGMENT_MULTIPLIERS = {
    "Occasional": 0.75,
    "Regular": 1.00,
    "Frequent": 1.25
}


# ============================================================
# DEMAND SPIKE PARAMETERS
# ============================================================

SURGE_PROBABILITY = 0.015

MIN_SURGE_MULTIPLIER = 1.20
MAX_SURGE_MULTIPLIER = 1.80


# ============================================================
# RANDOM NOISE
# ============================================================

NOISE_MIN = 0.90
NOISE_MAX = 1.10


# ============================================================
# RANDOM SEED
# ============================================================

RANDOM_SEED = 42


# ============================================================
# STEP 02.4.2 - CREATE HOURLY DEMAND TIMELINE
# ============================================================

import pandas as pd
from pathlib import Path


def create_hourly_timeline():
    """
    Create an hourly timeline for the complete study period
    and replicate it across all Hyderabad zones.
    """

    # Create hourly timestamps
    timestamps = pd.date_range(
        start=START_DATE,
        end=END_DATE,
        freq="h"
    )

    # Create one record for every timestamp-zone combination
    zone_records = []

    for timestamp in timestamps:

        for zone_id in ZONE_BASE_DEMAND.keys():

            zone_records.append({
                "timestamp": timestamp,
                "zone_id": zone_id
            })

    # Convert to DataFrame
    demand_df = pd.DataFrame(zone_records)

    # Add time-related features
    demand_df["date"] = demand_df["timestamp"].dt.date
    demand_df["hour"] = demand_df["timestamp"].dt.hour
    demand_df["day_of_week"] = demand_df["timestamp"].dt.dayofweek
    demand_df["day_name"] = demand_df["timestamp"].dt.day_name()
    demand_df["month"] = demand_df["timestamp"].dt.month

    return demand_df

# ============================================================
# STEP 02.4.3 - APPLY DEMAND PATTERNS
# ============================================================

def apply_demand_patterns(demand_df):
    """
    Apply baseline, hourly, weekly, and zone-level
    demand patterns to the hourly timeline.
    """

    # --------------------------------------------------------
    # 1. BASELINE DEMAND
    # --------------------------------------------------------

    demand_df["base_demand"] = demand_df["zone_id"].map(
        ZONE_BASE_DEMAND
    )

    # --------------------------------------------------------
    # 2. HOURLY SEASONALITY
    # --------------------------------------------------------

    demand_df["hour_multiplier"] = demand_df["hour"].map(
        HOUR_MULTIPLIERS
    )

    # --------------------------------------------------------
    # 3. WEEKLY SEASONALITY
    # --------------------------------------------------------

    demand_df["day_multiplier"] = demand_df["day_of_week"].map(
        DAY_MULTIPLIERS
    )

    # --------------------------------------------------------
    # 4. ZONE EFFECT
    # --------------------------------------------------------

    demand_df["zone_multiplier"] = demand_df["zone_id"].map(
        ZONE_MULTIPLIERS
    )

    # --------------------------------------------------------
    # 5. CALCULATE BASE EXPECTED DEMAND
    # --------------------------------------------------------

    demand_df["base_expected_demand"] = (
        demand_df["base_demand"]
        * demand_df["hour_multiplier"]
        * demand_df["day_multiplier"]
        * demand_df["zone_multiplier"]
    )

    return demand_df

# ============================================================
# STEP 02.4.4 - APPLY SEASONAL VARIATION
# ============================================================

def apply_seasonal_variation(demand_df):
    """
    Apply monthly seasonal variation to the expected demand.
    """

    # Map month to seasonal multiplier
    demand_df["seasonal_multiplier"] = demand_df["month"].map(
        MONTH_MULTIPLIERS
    )

    # Apply seasonal variation
    demand_df["seasonal_expected_demand"] = (
        demand_df["base_expected_demand"]
        * demand_df["seasonal_multiplier"]
    )

    return demand_df
        
    
# ============================================================
# MASTER DATA PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RESTAURANT_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "orders"
    / "restaurants.csv"
)

CUSTOMER_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "orders"
    / "customers.csv"
)


# ============================================================
# STEP 02.4.5.1 - LOAD MASTER DATA
# ============================================================

def load_master_data():
    """
    Load restaurant and customer master datasets.
    """

    restaurants = pd.read_csv(RESTAURANT_FILE)

    customers = pd.read_csv(CUSTOMER_FILE)

    print("\nMaster data loaded successfully!")

    print(f"Restaurants: {len(restaurants):,}")
    print(f"Customers: {len(customers):,}")

    return restaurants, customers


# ============================================================
# STEP 02.4.5.2 - CALCULATE ZONE BEHAVIORAL FACTORS
# ============================================================

def calculate_zone_behavior_factors(restaurants, customers):
    """
    Calculate synthetic behavioral factors for each zone
    using the restaurant and customer master datasets.
    """

    # --------------------------------------------------------
    # CUSTOMER ACTIVITY BY ZONE
    # --------------------------------------------------------

    customer_zone = (
        customers
        .groupby("home_zone_id")
        .agg(
            customer_count=("customer_id", "count"),
            avg_customer_activity=("customer_activity_score", "mean")
        )
        .reset_index()
    )

    # --------------------------------------------------------
    # RESTAURANT POPULARITY BY ZONE
    # --------------------------------------------------------

    restaurant_zone = (
        restaurants
        .groupby("zone_id")
        .agg(
            restaurant_count=("restaurant_id", "count"),
            avg_restaurant_popularity=("base_popularity", "mean")
        )
        .reset_index()
    )

    # --------------------------------------------------------
    # COMBINE ZONE FACTORS
    # --------------------------------------------------------

    zone_behavior = restaurant_zone.merge(
        customer_zone,
        left_on="zone_id",
        right_on="home_zone_id",
        how="left"
    )

    zone_behavior.drop(
        columns=["home_zone_id"],
        inplace=True
    )

    # --------------------------------------------------------
    # CUSTOMER BEHAVIOR FACTOR
    # --------------------------------------------------------

    zone_behavior["customer_behavior_factor"] = (
        0.85
        + zone_behavior["avg_customer_activity"] * 0.30
    )

    # --------------------------------------------------------
    # RESTAURANT EFFECT
    # --------------------------------------------------------

    zone_behavior["restaurant_effect"] = (
        0.90
        + zone_behavior["avg_restaurant_popularity"] * 0.20
    )

    return zone_behavior

# ============================================================
# STEP 02.4.5.3 - APPLY BEHAVIORAL EFFECTS
# ============================================================

def apply_behavioral_effects(
    demand_df,
    restaurants,
    customers
):
    """
    Apply customer and restaurant behavioral effects
    to the seasonal expected demand.
    """

    zone_behavior = calculate_zone_behavior_factors(
        restaurants,
        customers
    )

    demand_df = demand_df.merge(
        zone_behavior[
            [
                "zone_id",
                "customer_count",
                "restaurant_count",
                "avg_customer_activity",
                "avg_restaurant_popularity",
                "customer_behavior_factor",
                "restaurant_effect"
            ]
        ],
        on="zone_id",
        how="left"
    )

    # Apply behavioral effects
    demand_df["behavior_adjusted_demand"] = (
        demand_df["seasonal_expected_demand"]
        * demand_df["customer_behavior_factor"]
        * demand_df["restaurant_effect"]
    )

    return demand_df

# ============================================================
# STEP 02.4.6 - CONTROLLED DEMAND SURGES
# ============================================================

def add_surge_effect(demand_df):
    """
    Create controlled synthetic demand surge events.

    Surge events are generated independently of real-world
    contextual data such as weather, holidays, and IPL.
    """

    import numpy as np

    # Reproducible random generator
    rng = np.random.default_rng(RANDOM_SEED)

    # Start with no surge
    demand_df["surge_flag"] = 0
    demand_df["surge_multiplier"] = 1.0

    # Candidate rows
    candidate_indices = demand_df.index[
        demand_df["hour"].between(18, 22)
    ]

    # Number of candidate surge events
    n_candidates = len(candidate_indices)

    # Random probability for each candidate
    surge_random = rng.random(n_candidates)

    surge_mask = surge_random < SURGE_PROBABILITY

    selected_indices = candidate_indices[surge_mask]

    # Assign surge multipliers
    if len(selected_indices) > 0:

        demand_df.loc[
            selected_indices,
            "surge_flag"
        ] = 1

        demand_df.loc[
            selected_indices,
            "surge_multiplier"
        ] = rng.uniform(
            MIN_SURGE_MULTIPLIER,
            MAX_SURGE_MULTIPLIER,
            size=len(selected_indices)
        )

    # Apply surge
    demand_df["surge_adjusted_demand"] = (
        demand_df["behavior_adjusted_demand"]
        * demand_df["surge_multiplier"]
    )

    return demand_df

# ============================================================
# STEP 02.4.7 - STOCHASTIC NOISE
# ============================================================

def add_stochastic_noise(demand_df):
    """
    Add controlled stochastic variation to the
    surge-adjusted demand.

    The noise is multiplicative and reproducible.
    """

    import numpy as np

    rng = np.random.default_rng(RANDOM_SEED)

    # Generate multiplicative noise
    demand_df["noise_multiplier"] = rng.uniform(
        NOISE_MIN,
        NOISE_MAX,
        size=len(demand_df)
    )

    # Apply stochastic variation
    demand_df["realized_demand"] = (
        demand_df["surge_adjusted_demand"]
        * demand_df["noise_multiplier"]
    )

    # Demand cannot be negative
    demand_df["realized_demand"] = (
        demand_df["realized_demand"]
        .clip(lower=0)
    )

    return demand_df

# ============================================================
# TEST DEMAND + SEASONAL + BEHAVIORAL + SURGE EFFECTS
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # LOAD MASTER DATA
    # --------------------------------------------------------

    restaurants, customers = load_master_data()

    # --------------------------------------------------------
    # CREATE HOURLY TIMELINE
    # --------------------------------------------------------

    demand_df = create_hourly_timeline()

    # --------------------------------------------------------
    # APPLY BASE DEMAND PATTERNS
    # --------------------------------------------------------

    demand_df = apply_demand_patterns(demand_df)

    # --------------------------------------------------------
    # APPLY SEASONAL VARIATION
    # --------------------------------------------------------

    demand_df = apply_seasonal_variation(demand_df)

    # --------------------------------------------------------
    # APPLY RESTAURANT + CUSTOMER EFFECTS
    # --------------------------------------------------------

    demand_df = apply_behavioral_effects(
        demand_df,
        restaurants,
        customers
    )

    # --------------------------------------------------------
    # APPLY CONTROLLED SURGE EFFECT
    # --------------------------------------------------------

    demand_df = add_surge_effect(demand_df)
    
    demand_df = add_stochastic_noise(demand_df)

    # ========================================================
    # VALIDATION OUTPUT
    # ========================================================

    print("\n==============================================")
    print("SURGE MECHANISM VALIDATION")
    print("==============================================")

    print("\nSurge mechanism applied successfully!")

    # --------------------------------------------------------
    # NUMBER OF SURGE RECORDS
    # --------------------------------------------------------

    print("\nNumber of surge records:")

    print(
        demand_df["surge_flag"].sum()
    )

    # --------------------------------------------------------
    # SURGE PERCENTAGE
    # --------------------------------------------------------

    print("\nSurge percentage:")

    print(
        round(
            demand_df["surge_flag"].mean() * 100,
            3
        ),
        "%"
    )

    # --------------------------------------------------------
    # SURGE MULTIPLIER STATISTICS
    # --------------------------------------------------------

    print("\nSurge multiplier statistics:")

    print(
        demand_df.loc[
            demand_df["surge_flag"] == 1,
            "surge_multiplier"
        ].describe()
    )

    # --------------------------------------------------------
    # FINAL SURGE-ADJUSTED DEMAND STATISTICS
    # --------------------------------------------------------

    print("\nFinal demand statistics:")

    print(
        demand_df["surge_adjusted_demand"].describe()
    )

    # ========================================================
    # BEHAVIORAL VALIDATION
    # ========================================================

    print("\n==============================================")
    print("BEHAVIORAL EFFECT VALIDATION")
    print("==============================================")

    print("\nZone behavioral factors:")

    print(
        demand_df[
            [
                "zone_id",
                "customer_count",
                "restaurant_count",
                "avg_customer_activity",
                "avg_restaurant_popularity",
                "customer_behavior_factor",
                "restaurant_effect"
            ]
        ]
        .drop_duplicates()
        .sort_values("zone_id")
        .to_string(index=False)
    )

    print("\nBehavior-adjusted demand statistics:")

    print(
        demand_df["behavior_adjusted_demand"].describe()
    )
    
    # ========================================================
    # STOCHASTIC NOISE VALIDATION
    # ========================================================

    print("\n==============================================")
    print("STOCHASTIC NOISE VALIDATION")
    print("==============================================")

    print("\nNoise multiplier statistics:")

    print(
        demand_df["noise_multiplier"].describe()
    )

    print("\nRealized demand statistics:")

    print(
        demand_df["realized_demand"].describe()
    )

    print("\nNegative demand values:")

    print(
        (demand_df["realized_demand"] < 0).sum()
    )