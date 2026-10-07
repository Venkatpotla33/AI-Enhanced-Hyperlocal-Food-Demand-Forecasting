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
# CONVERT DEMAND TO INTEGER ORDER COUNTS
# ============================================================

def convert_demand_to_order_counts(
    demand_df
):
    """
    Convert continuous realized demand into
    integer food-order counts using probabilistic rounding.

    Example:
        21.20 -> approximately 21 orders
        21.80 -> approximately 22 orders

    This preserves the expected demand across
    a large synthetic dataset.
    """

    demand_df = demand_df.copy()

    # --------------------------------------------------------
    # Separate integer and fractional components
    # --------------------------------------------------------

    demand_floor = np.floor(
        demand_df["realized_demand"]
    )

    fractional_part = (
        demand_df["realized_demand"]
        - demand_floor
    )

    # --------------------------------------------------------
    # Generate random values
    # --------------------------------------------------------

    random_values = np.random.random(
        len(demand_df)
    )

    # --------------------------------------------------------
    # Probabilistic rounding
    # --------------------------------------------------------

    demand_df["order_count"] = (
        demand_floor
        + (
            random_values
            < fractional_part
        ).astype(int)
    )

    # --------------------------------------------------------
    # Ensure integer datatype
    # --------------------------------------------------------

    demand_df["order_count"] = (
        demand_df["order_count"]
        .astype(int)
    )

    print(
        "\nRealized demand converted to integer "
        "order counts successfully!"
    )

    return demand_df

# ============================================================
# GENERATE TRANSACTION-LEVEL ORDERS
# ============================================================

def generate_transaction_rows(demand_df):
    """
    Expand hourly zone-level order counts into
    individual transaction records.

    Each transaction receives a random timestamp
    within its corresponding hour.
    """

    rng = np.random.default_rng(RANDOM_SEED)

    transaction_records = []

    order_sequence = 1

    # --------------------------------------------------------
    # Process each hourly-zone record
    # --------------------------------------------------------

    for row in demand_df.itertuples(index=False):

        order_count = row.order_count

        if order_count <= 0:
            continue

        # ----------------------------------------------------
        # Generate random seconds within the hour
        # ----------------------------------------------------

        random_seconds = rng.integers(
            low=0,
            high=3600,
            size=order_count
        )

        # ----------------------------------------------------
        # Create individual transaction timestamps
        # ----------------------------------------------------

        for seconds in random_seconds:

            order_timestamp = (
                row.timestamp
                + pd.Timedelta(
                    seconds=int(seconds)
                )
            )

            transaction_records.append(
                {
                    "order_id": f"ORD{order_sequence:09d}",
                    "order_timestamp": order_timestamp,
                    "zone_id": row.zone_id,
                    "order_count_source": order_count
                }
            )

            order_sequence += 1

    # --------------------------------------------------------
    # Convert transactions to DataFrame
    # --------------------------------------------------------

    orders_df = pd.DataFrame(
        transaction_records
    )

    print(
        "\nTransaction-level records generated successfully!"
    )

    print(
        f"Total transactions: {len(orders_df):,}"
    )

    return orders_df

# ============================================================
# ASSIGN CUSTOMERS TO TRANSACTIONS
# ============================================================

def assign_customers_to_transactions(orders_df, customers):
    """
    Assign a synthetic customer to each transaction.

    Customers are selected from the same home zone as
    the transaction's order zone.

    Frequent customers receive higher selection probability
    than Regular and Occasional customers.
    """

    rng = np.random.default_rng(RANDOM_SEED)

    assigned_customer_ids = np.empty(
        len(orders_df),
        dtype=object
    )

    for zone_id in orders_df["zone_id"].unique():

        transaction_mask = (
            orders_df["zone_id"] == zone_id
        )

        transaction_count = transaction_mask.sum()

        zone_customers = customers[
            customers["home_zone_id"] == zone_id
        ].copy()

        if zone_customers.empty:
            raise ValueError(
                f"No customers found for zone {zone_id}"
            )

        # ----------------------------------------------------
        # Customer segment weights
        # ----------------------------------------------------

        segment_weights = {
            "Occasional": 1.0,
            "Regular": 2.0,
            "Frequent": 4.0
        }

        zone_customers["selection_weight"] = (
            zone_customers["customer_segment"]
            .map(segment_weights)
        )

        # Combine segment behavior with activity score
        zone_customers["selection_weight"] *= (
            0.5 + zone_customers["customer_activity_score"]
        )

        probabilities = (
            zone_customers["selection_weight"]
            / zone_customers["selection_weight"].sum()
        )

        selected_customers = rng.choice(
            zone_customers["customer_id"].values,
            size=transaction_count,
            replace=True,
            p=probabilities.values
        )

        assigned_customer_ids[transaction_mask] = (
            selected_customers
        )

    orders_df = orders_df.copy()

    orders_df["customer_id"] = (
        assigned_customer_ids
    )

    print(
        "\nCustomers assigned to transactions successfully!"
    )

    print(
        f"Transactions processed: {len(orders_df):,}"
    )

    print(
        f"Unique customers used: "
        f"{orders_df['customer_id'].nunique():,}"
    )

    return orders_df
# ============================================================
# ASSIGN RESTAURANTS TO TRANSACTIONS
# ============================================================

def assign_restaurants_to_transactions(
    orders_df,
    restaurants
):
    """
    Assign a synthetic restaurant to each transaction.

    Restaurants are selected from the same zone as the
    transaction.

    Restaurant selection probability is influenced by
    restaurant popularity.
    """

    rng = np.random.default_rng(
        RANDOM_SEED + 1
    )

    assigned_restaurant_ids = np.empty(
        len(orders_df),
        dtype=object
    )

    for zone_id in orders_df["zone_id"].unique():

        transaction_mask = (
            orders_df["zone_id"] == zone_id
        )

        transaction_count = (
            transaction_mask.sum()
        )

        zone_restaurants = restaurants[
            restaurants["zone_id"] == zone_id
        ].copy()

        if zone_restaurants.empty:
            raise ValueError(
                f"No restaurants found for zone {zone_id}"
            )

        # ----------------------------------------------------
        # Restaurant popularity as selection weight
        # ----------------------------------------------------

        zone_restaurants["selection_weight"] = (
            zone_restaurants["base_popularity"]
            .clip(lower=0.05)
        )

        probabilities = (
            zone_restaurants["selection_weight"]
            / zone_restaurants["selection_weight"].sum()
        )

        selected_restaurants = rng.choice(
            zone_restaurants["restaurant_id"].values,
            size=transaction_count,
            replace=True,
            p=probabilities.values
        )

        assigned_restaurant_ids[
            transaction_mask
        ] = selected_restaurants

    orders_df = orders_df.copy()

    orders_df["restaurant_id"] = (
        assigned_restaurant_ids
    )

    print(
        "\nRestaurants assigned to transactions successfully!"
    )

    print(
        f"Transactions processed: "
        f"{len(orders_df):,}"
    )

    print(
        f"Unique restaurants used: "
        f"{orders_df['restaurant_id'].nunique():,}"
    )

    return orders_df

# ============================================================
# GENERATE ORDER VALUES
# ============================================================

def generate_order_values(
    orders_df,
    restaurants,
    customers
):
    """
    Generate realistic transaction-level order values.

    Order value is influenced by:
    - Restaurant average order value
    - Customer preferred order value
    - Customer segment
    - Stochastic variation
    """

    rng = np.random.default_rng(
        RANDOM_SEED + 2
    )

    orders_df = orders_df.copy()

    # --------------------------------------------------------
    # Restaurant information
    # --------------------------------------------------------

    restaurant_values = restaurants[
        [
            "restaurant_id",
            "average_order_value"
        ]
    ].copy()

    restaurant_values = restaurant_values.rename(
        columns={
            "average_order_value":
            "restaurant_aov"
        }
    )

    orders_df = orders_df.merge(
        restaurant_values,
        on="restaurant_id",
        how="left",
        validate="many_to_one"
    )

    # --------------------------------------------------------
    # Customer information
    # --------------------------------------------------------

    customer_values = customers[
        [
            "customer_id",
            "preferred_order_value",
            "customer_segment"
        ]
    ].copy()

    orders_df = orders_df.merge(
        customer_values,
        on="customer_id",
        how="left",
        validate="many_to_one"
    )

    # --------------------------------------------------------
    # Validate master-data joins
    # --------------------------------------------------------

    if orders_df["restaurant_aov"].isna().any():
        raise ValueError(
            "Missing restaurant AOV after merge."
        )

    if orders_df["preferred_order_value"].isna().any():
        raise ValueError(
            "Missing customer preferred order value "
            "after merge."
        )

    # --------------------------------------------------------
    # Blend restaurant and customer preferences
    # --------------------------------------------------------

    base_order_value = (
        0.60 * orders_df["restaurant_aov"]
        +
        0.40 * orders_df["preferred_order_value"]
    )

    # --------------------------------------------------------
    # Customer segment effect
    # --------------------------------------------------------

    segment_multiplier = {
        "Occasional": 0.95,
        "Regular": 1.00,
        "Frequent": 1.05
    }

    orders_df["segment_multiplier"] = (
        orders_df["customer_segment"]
        .map(segment_multiplier)
        .fillna(1.0)
    )

    # --------------------------------------------------------
    # Stochastic variation
    # --------------------------------------------------------

    noise = rng.normal(
        loc=1.0,
        scale=0.08,
        size=len(orders_df)
    )

    noise = np.clip(
        noise,
        0.80,
        1.20
    )

    # --------------------------------------------------------
    # Final order value
    # --------------------------------------------------------

    orders_df["order_value"] = (
        base_order_value
        * orders_df["segment_multiplier"]
        * noise
    )

    # Round to realistic currency precision
    orders_df["order_value"] = (
        orders_df["order_value"]
        .round(2)
    )

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    if (orders_df["order_value"] <= 0).any():
        raise ValueError(
            "Non-positive order values detected."
        )

    print(
        "\nOrder values generated successfully!"
    )

    print(
        f"Mean order value: "
        f"₹{orders_df['order_value'].mean():.2f}"
    )

    print(
        f"Minimum order value: "
        f"₹{orders_df['order_value'].min():.2f}"
    )

    print(
        f"Maximum order value: "
        f"₹{orders_df['order_value'].max():.2f}"
    )

    return orders_df
# ============================================================
# ASSIGN MEAL PERIOD
# ============================================================

def assign_meal_period(orders_df):
    """
    Assign a meal period based on the transaction timestamp.
    """

    orders_df = orders_df.copy()

    hour = orders_df["order_timestamp"].dt.hour

    conditions = [
        hour.between(5, 8),
        hour.between(9, 11),
        hour.between(12, 14),
        hour.between(15, 17),
        hour.between(18, 19),
        hour.between(20, 22),
        hour.isin([23, 0, 1, 2, 3, 4])
    ]

    choices = [
        "Morning",
        "Late_Morning",
        "Lunch",
        "Afternoon",
        "Evening",
        "Dinner",
        "Late_Night"
    ]

    orders_df["meal_period"] = np.select(
        conditions,
        choices,
        default="Unknown"
    )

    print(
        "\nMeal periods assigned successfully!"
    )

    print(
        "\nMeal period distribution:"
    )

    print(
        orders_df["meal_period"]
        .value_counts()
        .sort_index()
    )

    return orders_df
# ============================================================
# ASSIGN DAY TYPE
# ============================================================

def assign_day_type(orders_df):
    """
    Assign weekday/weekend classification
    based on the order timestamp.
    """

    orders_df = orders_df.copy()

    day_of_week = orders_df["order_timestamp"].dt.dayofweek

    orders_df["day_type"] = np.where(
        day_of_week >= 5,
        "Weekend",
        "Weekday"
    )

    print(
        "\nDay type assigned successfully!"
    )

    print(
        "\nDay type distribution:"
    )

    print(
        orders_df["day_type"]
        .value_counts()
    )

    return orders_df

# ============================================================
# ASSIGN DAY OF WEEK
# ============================================================

def assign_day_of_week(orders_df):
    """
    Assign the day of week based on the order timestamp.
    """

    orders_df = orders_df.copy()

    orders_df["day_of_week"] = (
        orders_df["order_timestamp"]
        .dt.day_name()
    )

    print(
        "\nDay of week assigned successfully!"
    )

    print(
        "\nDay of week distribution:"
    )

    print(
        orders_df["day_of_week"]
        .value_counts()
    )

    return orders_df

# ============================================================
# ASSIGN CALENDAR PERIOD
# ============================================================

def assign_calendar_period(orders_df):
    """
    Extract calendar year and month from the order timestamp.
    """

    orders_df = orders_df.copy()

    orders_df["order_year"] = (
        orders_df["order_timestamp"].dt.year
    )

    orders_df["order_month"] = (
        orders_df["order_timestamp"].dt.month
    )

    orders_df["order_month_name"] = (
        orders_df["order_timestamp"].dt.month_name()
    )

    print(
        "\nCalendar period assigned successfully!"
    )

    print(
        "\nYear distribution:"
    )

    print(
        orders_df["order_year"]
        .value_counts()
        .sort_index()
    )

    print(
        "\nMonth distribution:"
    )

    print(
        orders_df["order_month_name"]
        .value_counts()
    )

    return orders_df

# ============================================================
# FINALIZE RAW TRANSACTION DATASET
# ============================================================

def finalize_raw_orders(orders_df):
    """
    Keep only the required transaction-level fields
    for the final raw synthetic order dataset.
    """

    final_columns = [
        "order_id",
        "order_timestamp",
        "zone_id",
        "customer_id",
        "restaurant_id",
        "order_value",
        "meal_period",
        "day_type",
        "day_of_week",
        "order_year",
        "order_month",
        "order_month_name"
    ]

    missing_columns = [
        column
        for column in final_columns
        if column not in orders_df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    orders_df = orders_df[
        final_columns
    ].copy()

    print(
        "\nRaw transaction dataset finalized!"
    )

    print(
        f"Rows: {len(orders_df):,}"
    )

    print(
        f"Columns: {len(orders_df.columns)}"
    )

    print(
        "\nFinal columns:"
    )

    for column in orders_df.columns:
        print(f"- {column}")

    return orders_df

# ============================================================
# VALIDATE TRANSACTION INTEGRITY
# ============================================================

def validate_transaction_integrity(
    orders_df,
    restaurants,
    customers
):
    """
    Perform final integrity checks on the
    transaction-level synthetic order dataset.
    """

    print(
        "\n=============================================="
    )

    print(
        "TRANSACTION INTEGRITY VALIDATION"
    )

    print(
        "=============================================="
    )

    # --------------------------------------------------------
    # 1. Order ID validation
    # --------------------------------------------------------

    duplicate_orders = (
        orders_df["order_id"]
        .duplicated()
        .sum()
    )

    print(
        f"\nDuplicate order IDs: {duplicate_orders:,}"
    )

    # --------------------------------------------------------
    # 2. Customer existence validation
    # --------------------------------------------------------

    valid_customers = set(
        customers["customer_id"]
    )

    missing_customers = (
        ~orders_df["customer_id"]
        .isin(valid_customers)
    ).sum()

    print(
        f"Missing customer IDs: "
        f"{missing_customers:,}"
    )

    # --------------------------------------------------------
    # 3. Restaurant existence validation
    # --------------------------------------------------------

    valid_restaurants = set(
        restaurants["restaurant_id"]
    )

    missing_restaurants = (
        ~orders_df["restaurant_id"]
        .isin(valid_restaurants)
    ).sum()

    print(
        f"Missing restaurant IDs: "
        f"{missing_restaurants:,}"
    )

    # --------------------------------------------------------
    # 4. Restaurant-zone consistency
    # --------------------------------------------------------

    restaurant_zone_map = (
        restaurants
        .set_index("restaurant_id")["zone_id"]
        .to_dict()
    )

    expected_restaurant_zones = (
        orders_df["restaurant_id"]
        .map(restaurant_zone_map)
    )

    restaurant_zone_mismatches = (
        expected_restaurant_zones
        != orders_df["zone_id"]
    ).sum()

    print(
        f"Restaurant-zone mismatches: "
        f"{restaurant_zone_mismatches:,}"
    )

    # --------------------------------------------------------
    # 5. Customer-zone consistency
    # --------------------------------------------------------

    customer_zone_map = (
        customers
        .set_index("customer_id")["home_zone_id"]
        .to_dict()
    )

    expected_customer_zones = (
        orders_df["customer_id"]
        .map(customer_zone_map)
    )

    customer_zone_mismatches = (
        expected_customer_zones
        != orders_df["zone_id"]
    ).sum()

    print(
        f"Customer-zone mismatches: "
        f"{customer_zone_mismatches:,}"
    )

    # --------------------------------------------------------
    # 6. Order value validation
    # --------------------------------------------------------

    invalid_order_values = (
        orders_df["order_value"] <= 0
    ).sum()

    print(
        f"Invalid order values: "
        f"{invalid_order_values:,}"
    )

    # --------------------------------------------------------
    # 7. Timestamp validation
    # --------------------------------------------------------

    min_timestamp = (
        orders_df["order_timestamp"].min()
    )

    max_timestamp = (
        orders_df["order_timestamp"].max()
    )

    print(
        f"\nMinimum timestamp: "
        f"{min_timestamp}"
    )

    print(
        f"Maximum timestamp: "
        f"{max_timestamp}"
    )

    # --------------------------------------------------------
    # 8. Missing-value validation
    # --------------------------------------------------------

    total_missing = (
        orders_df.isna().sum().sum()
    )

    print(
        f"\nTotal missing values: "
        f"{total_missing:,}"
    )

    # --------------------------------------------------------
    # Final status
    # --------------------------------------------------------

    if (
        duplicate_orders == 0
        and missing_customers == 0
        and missing_restaurants == 0
        and restaurant_zone_mismatches == 0
        and customer_zone_mismatches == 0
        and invalid_order_values == 0
        and total_missing == 0
    ):

        print(
            "\n✅ TRANSACTION INTEGRITY CHECK PASSED"
        )

    else:

        print(
            "\n❌ TRANSACTION INTEGRITY CHECK FAILED"
        )

    return orders_df

# ============================================================
# SAVE RAW TRANSACTION DATASET
# ============================================================

def save_raw_orders(orders_df):
    """
    Save the finalized transaction-level synthetic
    food order dataset.
    """

    output_file = (
        RAW_ORDERS_DIR / "orders.csv"
    )

    print(
        "\nSaving raw transaction dataset..."
    )

    orders_df.to_csv(
        output_file,
        index=False
    )

    print(
        "\nRaw transaction dataset saved successfully!"
    )

    print(
        f"File: {output_file}"
    )

    print(
        f"Rows: {len(orders_df):,}"
    )

    print(
        f"Columns: {len(orders_df.columns)}"
    )

    return output_file

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
    # CONVERT DEMAND TO ORDER COUNTS
    # --------------------------------------------------------

    demand_df = convert_demand_to_order_counts(
        demand_df
    )

    # ========================================================
    # VALIDATION
    # ========================================================

    print(
        "\n=============================================="
    )

    print(
        "ORDER COUNT VALIDATION"
    )

    print(
        "=============================================="
    )

    print(
        "\nFirst 10 demand-to-order conversions:"
    )

    print(
        demand_df[
            [
                "timestamp",
                "zone_id",
                "realized_demand",
                "order_count"
            ]
        ]
        .head(10)
        .to_string(index=False)
    )

    print(
        "\nOrder count statistics:"
    )

    print(
        demand_df[
            "order_count"
        ].describe()
    )

    print(
        "\nOrder count datatype:"
    )

    print(
        demand_df[
            "order_count"
        ].dtype
    )

    print(
        "\nZero-order records:"
    )

    print(
        (
            demand_df[
                "order_count"
            ] == 0
        ).sum()
    )

    print(
        "\nNegative order counts:"
    )

    print(
        (
            demand_df[
                "order_count"
            ] < 0
        ).sum()
    )
    
    # --------------------------------------------------------
    # GENERATE TRANSACTION ROWS
    # --------------------------------------------------------

    orders_df = generate_transaction_rows(
        demand_df
    )
    orders_df = assign_customers_to_transactions(
        orders_df,
        customers
    )
    orders_df = assign_restaurants_to_transactions(
        orders_df,
        restaurants
    )
    orders_df = generate_order_values(
        orders_df,
        restaurants,
        customers
    )
    orders_df = assign_meal_period(
        orders_df
    )
    orders_df = assign_day_type(
        orders_df
    )
    orders_df = assign_day_of_week(
        orders_df
    )
    orders_df = assign_calendar_period(
        orders_df
    )
    orders_df = finalize_raw_orders(
        orders_df
    )
    orders_df = validate_transaction_integrity(
        orders_df,
        restaurants,
        customers
    )
    output_file = save_raw_orders(
        orders_df
    )

    print(
        "\n=============================================="
    )

    print(
        "RAW ORDER DATASET COMPLETE"
    )

    print(
        "=============================================="
    )

    print(
        f"\nSaved file:"
    )

    print(
        output_file
    )

    print(
        "\n=============================================="
    )

    print(
        "FINAL RAW ORDER VALIDATION"
    )

    print(
        "=============================================="
    )

    print(
        "\nDataset shape:"
    )

    print(
        orders_df.shape
    )

    print(
        "\nFirst 10 final transactions:"
    )

    print(
        orders_df.head(10).to_string(
            index=False
        )
    )

    print(
        "\nMissing values:"
    )

    print(
        orders_df.isna().sum()
    )

    print(
        "\nDuplicate order IDs:"
    )

    print(
        orders_df["order_id"]
        .duplicated()
        .sum()
    )

    print(
        "\n=============================================="
    )

    print(
        "CALENDAR PERIOD VALIDATION"
    )

    print(
        "=============================================="
    )

    print(
        "\nFirst 10 transactions:"
    )

    print(
        orders_df[
            [
                "order_id",
                "order_timestamp",
                "zone_id",
                "customer_id",
                "restaurant_id",
                "order_value",
                "meal_period",
                "day_type",
                "day_of_week",
                "order_year",
                "order_month",
                "order_month_name"
            ]
        ]
        .head(10)
        .to_string(index=False)
    )

    print(
        "\nMissing years:"
    )

    print(
        orders_df["order_year"].isna().sum()
    )

    print(
        "\nMissing months:"
    )

    print(
        orders_df["order_month"].isna().sum()
    )

    print(
        "\n=============================================="
    )

    print(
        "DAY OF WEEK VALIDATION"
    )

    print(
        "=============================================="
    )

    print(
        "\nFirst 10 transactions:"
    )

    print(
        orders_df[
            [
                "order_id",
                "order_timestamp",
                "zone_id",
                "customer_id",
                "restaurant_id",
                "order_value",
                "meal_period",
                "day_type",
                "day_of_week"
            ]
        ]
        .head(10)
        .to_string(index=False)
    )

    print(
        "\nMissing day of week:"
    )

    print(
        orders_df["day_of_week"].isna().sum()
    )

    print(
        "\n=============================================="
    )

    print(
        "DAY TYPE VALIDATION"
    )

    print(
        "=============================================="
    )

    print(
        "\nFirst 10 transactions:"
    )

    print(
        orders_df[
            [
                "order_id",
                "order_timestamp",
                "zone_id",
                "customer_id",
                "restaurant_id",
                "order_value",
                "meal_period",
                "day_type"
            ]
        ]
        .head(10)
        .to_string(index=False)
    )

    print(
        "\nMissing day types:"
    )

    print(
        orders_df["day_type"].isna().sum()
    )

    print(
        "\n=============================================="
    )

    print(
        "MEAL PERIOD VALIDATION"
    )

    print(
        "=============================================="
    )

    print(
        "\nFirst 10 transactions:"
    )

    print(
        orders_df[
            [
                "order_id",
                "order_timestamp",
                "zone_id",
                "customer_id",
                "restaurant_id",
                "order_value",
                "meal_period"
            ]
        ]
        .head(10)
        .to_string(index=False)
    )

    print(
        "\nMissing meal periods:"
    )

    print(
        orders_df["meal_period"].isna().sum()
    )

    print(
        "\n=============================================="
    )

    print(
        "ORDER VALUE VALIDATION"
    )

    print(
        "=============================================="
    )

    print(
        "\nFirst 10 transactions:"
    )

    print(
        orders_df[
            [
                "order_id",
                "order_timestamp",
                "zone_id",
                "customer_id",
                "restaurant_id",
                "order_value"
            ]
        ]
        .head(10)
        .to_string(index=False)
    )

    print(
        "\nOrder value statistics:"
    )

    print(
        orders_df["order_value"].describe()
    )

    print(
        "\nMissing order values:"
    )

    print(
        orders_df["order_value"].isna().sum()
    )

    print(
        "\n=============================================="
    )

    print(
        "RESTAURANT ASSIGNMENT VALIDATION"
    )

    print(
        "=============================================="
    )

    print(
        "\nFirst 10 transactions:"
    )

    print(
        orders_df[
            [
                "order_id",
                "order_timestamp",
                "zone_id",
                "customer_id",
                "restaurant_id"
            ]
        ]
        .head(10)
        .to_string(index=False)
    )

    print(
        "\nUnique restaurants used:"
    )

    print(
        orders_df["restaurant_id"].nunique()
    )

    print(
        "\nMissing restaurant IDs:"
    )

    print(
        orders_df["restaurant_id"].isna().sum()
    )

    print(
        "\n=============================================="
    )
    print(
        "CUSTOMER ASSIGNMENT VALIDATION"
    )
    print(
        "=============================================="
    )

    print(
        "\nFirst 10 transactions with customers:"
    )

    print(
        orders_df[
            [
                "order_id",
                "order_timestamp",
                "zone_id",
                "customer_id"
                
            ]
        ]
        .head(10)
        .to_string(index=False)
    )

    print(
        "\nUnique customers used:"
    )

    print(
        orders_df["customer_id"].nunique()
    )

    print(
        "\nMissing customer IDs:"
    )

    print(
        orders_df["customer_id"].isna().sum()
    )

    # ========================================================
    # TRANSACTION VALIDATION
    # ========================================================

    print(
        "\n=============================================="
    )

    print(
        "TRANSACTION GENERATION VALIDATION"
    )

    print(
        "=============================================="
    )

    print(
        "\nFirst 10 transactions:"
    )

    print(
        orders_df.head(10).to_string(
            index=False
        )
    )

    print(
        "\nTransaction dataset shape:"
    )

    print(
        orders_df.shape
    )

    print(
        "\nUnique order IDs:"
    )

    print(
        orders_df["order_id"].nunique()
    )

    print(
        "\nDuplicate order IDs:"
    )

    print(
        orders_df["order_id"].duplicated().sum()
    )