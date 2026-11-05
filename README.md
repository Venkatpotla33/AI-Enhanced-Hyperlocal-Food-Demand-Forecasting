# 🚀 AI-Enhanced Hyperlocal Food Demand Forecasting and Surge Intelligence

## 📌 Project Title

**AI-Enhanced Hyperlocal Food Demand Forecasting and Surge Intelligence Using Machine Learning, Deep Learning, and Time-Series Foundation Models**

---

## 🎯 Overview

This project develops an AI-enhanced hyperlocal food demand forecasting system for food-delivery operations in Hyderabad, India.

The system focuses on forecasting **hourly food-order demand at hyperlocal zone level** and identifying potential demand-surge conditions using historical demand patterns and contextual factors.

The project compares multiple generations of forecasting approaches, including:

* Classical statistical models
* Machine learning models
* Deep learning models
* Time-series foundation models

An additional **AI Surge Intelligence Layer** is developed to interpret forecast outputs, identify potential demand surges, analyze contextual signals, and generate operational insights.

---

## 🔬 Research Problem

Food-delivery demand varies significantly across time and location.

Hourly demand can be influenced by:

* 🕐 Time of day
* 📅 Day of week
* 🗓️ Weekdays and weekends
* 🌦️ Weather
* 🌧️ Rainfall
* 🎉 Public holidays and festivals
* 🏏 IPL matches
* 📍 Local events
* 🏟️ Sporting events
* 🏙️ Zone-specific characteristics

Accurately forecasting demand at a hyperlocal level can help identify periods of potential demand-supply imbalance.

This project investigates whether different forecasting approaches can accurately predict localized hourly food demand and whether contextual information can improve forecasting and surge intelligence.

---

## 🎯 Objectives

### Primary Objective

Develop an AI-enhanced hyperlocal food demand forecasting system capable of predicting hourly food demand across delivery zones in Hyderabad.

### Secondary Objectives

1. Generate realistic synthetic food-order data for research purposes.
2. Develop a reproducible synthetic demand-generation methodology.
3. Collect historical contextual information from authorized sources and APIs.
4. Construct hourly zone-level demand time series.
5. Compare classical, machine learning, deep learning, and time-series foundation models.
6. Evaluate forecasting performance using rolling-origin backtesting.
7. Investigate the contribution of contextual features.
8. Develop an AI layer for demand-surge intelligence.
9. Provide interpretable forecast and contextual insights.
10. Build interactive visualization and demonstration applications.

---

## 📊 Data Strategy

### 🧾 Synthetic Order Data

The order dataset is synthetically generated for Hyderabad covering:

**January 2023 to August 2026**

The synthetic order-generation framework does not rely on simple random order counts.

Instead, demand is generated using a stochastic framework incorporating:

* Baseline demand
* Hourly seasonality
* Weekly seasonality
* Zone-specific demand patterns
* Restaurant characteristics
* Customer behavior
* Seasonal variation
* Controlled demand spikes
* Random/stochastic noise

### 📈 Current Dataset

| Component              |                Quantity |
| ---------------------- | ----------------------: |
| Synthetic Transactions |          **17,188,957** |
| Customers              |              **50,000** |
| Restaurants            |                 **220** |
| Hyperlocal Zones       |                   **5** |
| Raw Dataset Period     | **Jan 2023 – Aug 2026** |

The raw transaction dataset is maintained locally and excluded from GitHub because of its large size.

---

## 🌦️ Real Contextual Data

Contextual datasets have been collected and prepared independently from the synthetic order dataset.

The contextual variables include:

* Weather
* Rainfall
* Public holidays
* Festivals
* IPL schedules
* Local events
* Sporting events
* Day-specific patterns

> **Research Design:** Synthetic food-order demand is generated independently of the later contextual datasets to reduce circularity and avoid directly embedding future predictor variables into the synthetic demand-generation process.

### Contextual Data Integration

Phase 04 successfully integrated the contextual features with the existing hourly food-demand dataset.

The contextual datasets were cleaned, standardized, validated, and transformed into zone-aware hourly features before integration.

| Contextual Dataset            | Final Records |
| ----------------------------- | ------------: |
| Historical Weather            |        31,392 |
| Public Holidays and Festivals |           182 |
| Cricket Events                |         8,546 |
| Sporting Events               |            67 |
| Hyderabad Local Events        |           534 |

The final integrated dataset contains:

| Component                   |      Result |
| --------------------------- | ----------: |
| Integrated Hourly Records   | **156,960** |
| Total Columns               |      **34** |
| Hyperlocal Zones            |       **5** |
| Records per Zone            |  **31,392** |
| Duplicate Zone-Time Keys    |       **0** |
| Missing Hourly Zone Records |       **0** |

**Final contextual integration study period: January 1, 2023 – July 31, 2026.**

August 2026 transactions remain in the original raw orders dataset but are excluded from the final integrated modelling dataset.

The final integrated dataset is maintained locally because of its size and is excluded from GitHub.

---

## 📍 Hyperlocal Zones

The current study uses five synthetic research zones in Hyderabad:

| Zone ID | Zone        |
| ------- | ----------- |
| Z01     | Kondapur    |
| Z02     | Hitech City |
| Z03     | Gachibowli  |
| Z04     | Madhapur    |
| Z05     | Kukatpally  |

The zone configuration is maintained in:

[`config/zones.yaml`](config/zones.yaml)

> These zones represent synthetic research regions and do not represent official administrative or delivery boundaries.

---

## ✅ Data Quality & Validation

The generated transaction dataset has undergone structured data-quality and statistical validation.

| Validation Area                   | Status     |
| --------------------------------- | ---------- |
| Schema Validation                 | ✅ PASS     |
| Missing Value Validation          | ✅ PASS     |
| Duplicate & Identifier Validation | ✅ PASS     |
| Timestamp Validation              | ✅ PASS     |
| Value & Range Validation          | ✅ PASS     |
| Referential Integrity             | ✅ PASS     |
| Distribution Validation           | ✅ PASS     |
| Statistical Summary               | ✅ PASS     |
| **Overall Data Quality**          | **✅ PASS** |

### Dataset Integrity

* **17,188,957** unique orders
* **0** duplicate order IDs
* **0** missing values
* **0** invalid timestamps
* **0** customer-zone mismatches
* **0** restaurant-zone mismatches
* **50,000** unique customers
* **220** unique restaurants
* **5** hyperlocal zones

Detailed validation is documented in:

[`notebooks/02_data_quality_analysis.ipynb`](notebooks/02_data_quality_analysis.ipynb)

### Contextual Integration Validation

The final integrated dataset underwent additional validation.

| Integration Validation           | Status |
| -------------------------------- | ------ |
| Expected Integrated Record Count | ✅ PASS |
| Invalid Integrated Timestamps    | ✅ PASS |
| Timestamps Outside Study Period  | ✅ PASS |
| All Expected Zones Present       | ✅ PASS |
| Unexpected Zones                 | ✅ PASS |
| Duplicate Timestamp-Zone Keys    | ✅ PASS |
| Complete Hourly Zone Coverage    | ✅ PASS |
| Demand Reconciliation            | ✅ PASS |
| Negative Demand Values           | ✅ PASS |

**Demand Reconciliation:**

* Original aggregated demand: 16,795,775
* Integrated demand total: 16,795,775
* Mismatched demand records: 0

All final Phase 04 integration validation checks passed.

---

## 📊 Exploratory Data Analysis

Phase 03 — Data Quality & Exploratory Analysis has been completed.

The EDA covered transaction and order-value distributions, meal-period demand, hourly and daily patterns, weekday/weekend comparisons, weekly and monthly trends, zone-level demand and variability, autocorrelation, stationarity, seasonal decomposition, and hourly panel validation.

Key findings from the synthetic dataset include:

* **Peak demand hour:** 21:00
* **Lowest-demand hour:** 03:00
* **Lunch and dinner share:** Approximately 48.05% of transactions
* **Weekend demand:** Approximately 13.8% higher average daily demand than weekdays
* **Highest-demand zone:** Z02 — Hitech City
* **Hourly observations:** 160,560 across five zones
* **Hourly panel validation:** Passed, with no missing hourly intervals or duplicate zone-hour combinations in the complete-date panel

The complete-date hourly panel covers January 1, 2023, through August 30, 2026. August 31, 2026, is excluded because it is an incomplete date.

These findings describe the synthetic dataset and should not be interpreted as verified real-world Hyderabad food-delivery patterns.

Detailed findings are documented in:

[`docs/03_data_quality_and_exploratory_analysis.md`](docs/03_data_quality_and_exploratory_analysis.md)

---

## 🔄 Phase 04 – Contextual Data Collection & Integration

Phase 04 — Contextual Data Collection, Preparation and Integration has been completed.

The objective was to enrich the existing synthetic food-demand dataset with external contextual variables and construct an integrated hourly zone-level dataset.

### Phase 04 Workflow

| Subphase    | Description                               | Status      |
| ----------- | ----------------------------------------- | ----------- |
| Phase 04.1  | Raw Contextual Data Inspection            | ✅ Completed |
| Phase 04.2  | Contextual Source Evaluation              | ✅ Completed |
| Phase 04.3  | Historical Weather Data Preparation       | ✅ Completed |
| Phase 04.4  | Public Holidays and Festivals             | ✅ Completed |
| Phase 04.5  | Sports Events Collection                  | ✅ Completed |
| Phase 04.6  | Local Events Collection                   | ✅ Completed |
| Phase 04.7  | Local Events Validation                   | ✅ Completed |
| Phase 04.8  | Historical Contextual Data Preparation    | ✅ Completed |
| Phase 04.9  | Zone-Aware Contextual Feature Engineering | ✅ Completed |
| Phase 04.10 | Contextual Data Integration               | ✅ Completed |
| Phase 04.11 | Reproducible Data Pipeline                | ✅ Completed |
| Phase 04.12 | Integration Testing and Validation        | ✅ Completed |
| Phase 04.13 | Final Documentation and Handover          | ✅ Completed |

### Phase 04 Key Deliverables

* Cleaned contextual datasets
* Zone-aware contextual feature dataset
* Final integrated hourly demand dataset
* Corrected holiday feature mapping
* Reproducible data pipeline manifest
* Pipeline metadata
* Integration validation reports
* Final technical documentation and handover

**Primary Output:**

`Integrated_Contextual_Demand_Final.csv`

**Output Directory:**

`data/processed/phase_04_10_contextual_integration/`

**Final Status: ✅ PHASE 04 COMPLETED**

---

## 📌 Project Development Progress

| Phase    | Description                              | Status      |
| -------- | ---------------------------------------- | ----------- |
| Phase 01 | Project Framework & Repository Setup     | ✅ Completed |
| Phase 02 | Synthetic Raw Order Data Generation      | ✅ Completed |
| Phase 03 | Data Quality & Exploratory Analysis      | ✅ Completed |
| Phase 04 | Contextual Data Collection & Integration | ✅ Completed |
| Phase 05 | Feature Engineering                      | ⏳ Upcoming  |
| Phase 06 | Forecasting Models                       | ⏳ Upcoming  |
| Phase 07 | Model Evaluation & Backtesting           | ⏳ Upcoming  |
| Phase 08 | AI Surge Intelligence Layer              | ⏳ Upcoming  |
| Phase 09 | Power BI Dashboard                       | ⏳ Upcoming  |
| Phase 10 | Streamlit Application                    | ⏳ Upcoming  |
| Phase 11 | Research Analysis & Conclusions          | ⏳ Upcoming  |
| Phase 12 | Final Documentation                      | ⏳ Upcoming  |
