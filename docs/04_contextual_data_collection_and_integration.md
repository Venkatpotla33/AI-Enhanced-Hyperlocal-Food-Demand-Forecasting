# Phase 04 – Contextual Data Collection and Integration

## 1. Objective

The objective of Phase 04 was to collect, prepare, engineer,
and integrate contextual information with the existing
food-delivery order dataset.

The purpose is to create a unified hourly zone-level dataset
for subsequent food-demand forecasting experiments.

## 2. Study Scope

- Geographic scope: Hyderabad, India
- Study period: 01 January 2023 – 31 July 2026
- Time resolution: Hourly
- Timezone: Indian Standard Time (IST)
- Number of zones: 5

### Hyperlocal zones

| Zone ID | Zone |
|---|---|
| Z01 | Kondapur |
| Z02 | Hitech City |
| Z03 | Gachibowli |
| Z04 | Madhapur |
| Z05 | Kukatpally |

## 3. Contextual Data Sources

The following contextual categories were prepared:

1. Historical weather observations
2. Indian public holidays and regional festivals
3. Cricket matches, including IPL and international matches
4. Sporting events
5. Hyderabad local events

Traffic data was deferred and was not included in the
current integration.

## 4. Phase 04.8 – Historical Contextual Data Preparation

The collected datasets were inspected, standardized,
cleaned, validated, and saved separately.

| Dataset | Final Records |
|---|---:|
| Weather | 31,392 |
| Public Holidays and Festivals | 182 |
| Cricket | 8,546 |
| Sporting Events | 67 |
| Hyderabad Local Events | 534 |

The original source datasets were preserved.

Date and time fields were standardized for the study period.
Invalid dates, duplicates, missing values, and source-specific
data-quality conditions were examined.

Missing rainfall was not automatically interpreted as zero.

## 5. Phase 04.9 – Zone-Aware Contextual Feature Engineering

Contextual variables were transformed into an hourly
zone-aware feature dataset.

The generated dataset contains:

- 156,960 records
- 5 hyperlocal zones
- 31,392 hourly timestamps per zone
- 29 contextual feature columns

Weather, calendar, cricket, sporting-event, and local-event
features were aligned with the hourly zone-level structure.

## 6. Phase 04.10 – Contextual Data Integration

The original transaction dataset was aggregated to hourly
zone-level demand and integrated with the contextual features.

Integration keys:

- timestamp
- zone_id

The final integrated dataset contains:

- 156,960 records
- 34 columns
- 5 zones
- 31,392 hourly timestamps per zone

The target demand variable is order_count.

### Holiday feature mapping

The initial integration audit identified incomplete
holiday classification fields.

The holiday source was inspected and the calendar
classification was mapped using the available source fields.

The corrected integration retained fixed and optional
holiday distinctions.

Missing holiday names and classifications on non-holiday
hours should be interpreted in the context of event
occurrence, rather than automatically treated as data errors.

## 7. Phase 04.11 – Reproducible Data Pipeline

A reproducible data workflow and manifest were generated.

The workflow records the input datasets, processed
datasets, integrated output, file sizes, row counts,
column counts, and SHA-256 checksums.

The original orders and raw contextual sources remain
separate from the processed outputs.

The pipeline manifest and metadata are stored under:

data/processed/phase_04_11_pipeline_manifest/

## 8. Phase 04.12 – Integration Testing and Validation

The final integration validation passed all nine checks.

| Validation | Result |
|---|---|
| Expected integrated record count | PASS |
| No invalid timestamps | PASS |
| No timestamps outside study period | PASS |
| All expected zones present | PASS |
| No unexpected zones | PASS |
| No duplicate timestamp-zone keys | PASS |
| Complete hourly zone coverage | PASS |
| Demand reconciliation | PASS |
| No negative demand values | PASS |

### Demand reconciliation

Original aggregated demand: 16,795,775

Integrated demand: 16,795,775

Demand mismatches: 0

Five integrated-only timestamp-zone combinations were
confirmed to have zero demand. These valid zero-demand
observations were retained to preserve complete hourly
coverage.

## 9. Final Dataset

Final output:

data/processed/phase_04_10_contextual_integration/
corrected_holiday_mapping/Integrated_Contextual_Demand_Final.csv

Dataset dimensions:

- Rows: 156,960
- Columns: 34
- Zones: 5
- Time resolution: Hourly
- Study period: 01 January 2023 – 31 July 2026

The dataset is the primary integrated input for the
subsequent forecasting preparation and experiments.

## 10. Research Limitations

1. The food-delivery order dataset is synthetic and does
   not represent verified actual platform transactions.

2. Contextual integration establishes temporal alignment
   and enables predictive evaluation; it does not establish
   causal effects on demand.

3. Historical weather observations and event schedules
   may have source-specific coverage and limitations.

4. Event indicators represent recorded contextual events.
   They do not directly measure their actual influence
   on customer ordering behaviour.

5. Forecast-time availability of contextual variables
   must be considered to prevent temporal leakage.

6. Missing event attributes outside event periods may be
   structurally expected and must be interpreted according
   to feature semantics.

7. Traffic data was deferred from this phase.

## 11. Phase 04 Conclusion

Phase 04 established the contextual data preparation,
zone-aware feature engineering, integration, reproducibility,
and validation workflow.

The final integrated hourly dataset passed all nine
integration validation checks.

Phase 04 is ready for closure.

The next stage is Phase 05 – Forecasting Feature
Engineering and Preparation, subject to the approved
project roadmap.
