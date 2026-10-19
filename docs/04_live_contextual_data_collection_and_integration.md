# Phase 04 — Live Real-Time Contextual Data Collection and Integration

## 1. Purpose

Phase 04 prepares the Food Demand Forecasting Engine to use genuine external contextual information alongside the project's existing synthetic food-demand data. The goal is to establish a reproducible contextual-data workflow and a foundation for a live forecasting prototype.

The project will investigate live weather and weather forecasts, public holidays, festivals, sports events, concerts, exhibitions, conferences, and relevant local events.

> **Data transparency:** Food-order demand in this project is synthetic. Contextual records collected from external sources may be genuine, but combining them with synthetic demand does not turn the demand records into real customer transactions or prove real-world causal relationships.

## 2. Existing project assets

The project currently has completed work for data generation and exploratory analysis. The visible repository structure includes:

- `notebooks/01_data_generation.ipynb`
- `notebooks/02_data_quality_analysis.ipynb`
- `notebooks/03_exploratory_data_analysis.ipynb`
- `docs/01_project_framework.md`
- `docs/03_phase_final_summary.md`
- Data-generation scripts under `src/data_generation/`

The exact validated panel path, its schema, and the current state of any contextual-data directories must be verified during Step 04.1. Do not assume paths or column names before inspection.

## 3. Objectives

1. Inspect the existing repository, notebooks, data schemas, and configuration.
2. Evaluate reliable and permitted sources for live and historical contextual information.
3. Collect current weather conditions and available weather forecasts.
4. Prepare verified holiday and festival information.
5. Collect relevant sports schedules and event information.
6. Collect suitable local-event information, including concerts, exhibitions, conferences, and public gatherings.
7. Validate data quality, source provenance, timestamps, time zones, units, duplicates, and missingness.
8. Investigate historical contextual coverage for retrospective model evaluation.
9. prepare zone-aware and hourly contextual features for the five Hyderabad zones.
10. Integrate historical contextual features with the validated hourly demand panel without changing demand values or multiplying rows.
11. Build and test a refreshable live-context ingestion pipeline.
12. Document results, limitations, and the handover to Phase 05.

## 4. Geographic scope

The project's five synthetic hyperlocal zones are:

- `Z01` — Kondapur
- `Z02` — Hitech City
- `Z03` — Gachibowli
- `Z04` — Madhapur
- `Z05` — Kukatpally

Zone coordinates and boundaries must be verified from the existing project configuration or documented source. Do not invent zone coordinates. If a weather source provides only city-level or coarse-grid data, document that resolution and do not describe it as precise zone-level observation.

## 5. Data streams

### 5.1 Weather

Potential fields, depending on source availability:

- observation or forecast timestamp
- retrieval timestamp
- latitude and longitude or source grid identifier
- temperature
- apparent temperature
- relative humidity
- precipitation
- wind speed
- weather condition/code
- units, provider, and source metadata

Current observations and forecasts must be stored and labelled separately. Historical observations or reanalysis must also be labelled accurately; modelled/reanalysis values must not be described as direct station measurements unless the source confirms that.

### 5.2 Holidays and festivals

Potential fields:

- event date
- event name
- category
- geographic relevance
- official source
- publication/retrieval timestamp
- verification status
- notes and limitations

Public holidays, optional holidays, religious festivals, and local public gatherings are different categories and must not be silently treated as equivalent.

### 5.3 Sports and local events

Potential fields:

- source event identifier, if available
- event name and category
- scheduled start and end time, when available
- venue and address
- coordinates, when verified
- event status
- attendance/scale only when reliably published
- source URL or source reference
- first-seen and last-checked timestamps

Sports, concerts, exhibitions, conferences, and public gatherings should be represented in a common event schema where practical, while preserving source-specific fields when necessary. Respect source terms, rate limits, licensing, and access restrictions.

## 6. Historical research and live pipeline

Phase 04 will maintain two related but distinct data workflows.

### A. Historical research dataset

The existing synthetic demand panel spans complete dates from 2023-01-01 through 2026-08-30. Historical contextual information must align to the same timestamps to be used in retrospective evaluation.

Live observations collected now cannot be joined to historical timestamps as if they described past conditions. We will obtain historical contextual records from appropriate sources where available and document coverage gaps.

### B. Live contextual pipeline

The live pipeline will retrieve current conditions, available forecasts, and updated event/calendar information. It will record retrieval times and handle API errors, stale data, missing values, and source changes.

A live prototype using synthetic demand history is not, by itself, evidence of accurate real-world food-order forecasting. Validation against real customer orders would require appropriately authorized genuine demand data.

## 7. Leakage prevention

Forecasting features must contain only information that would have been available at the forecast issuance time.

For example, a forecast issued at 17:00 for 20:00 may use a weather forecast available at 17:00, but must not use the actual weather observation recorded at 20:00. Likewise, event cancellations and schedule changes must be handled according to when that information became available, where such timestamps can be established.

Historical backtesting should use chronological splits and avoid using future information to construct features.

## 8. Data quality and integration checks

For each source, document and validate:

- source identity, URL/API, retrieval time, access method, and license/terms
- coverage period and update frequency
- schema, data types, units, and time zone
- missing values, duplicate records, invalid values, and stale data
- event verification and schedule changes
- geographic resolution and zone-mapping assumptions
- join keys and join cardinality

Before and after integration, verify:

- expected number of zone-hour rows is preserved
- zone-hour keys remain unique
- demand values are unchanged
- joins do not multiply rows
- contextual missingness is measured and documented
- missing rainfall or other measurements are not silently converted to zero

## 9. Working protocol

Each subsection will follow this workflow:

1. Markdown explanation
2. Code
3. Execute the code and inspect actual output
4. Explain and interpret the output
5. Record findings and decisions in Markdown

Work one subsection at a time. Do not claim that code ran unless it was executed and its output inspected. Reuse validated assets and avoid unnecessary regeneration or repeated exploratory analysis.

## 10. Phase 04 work plan

| Step | Subsection | Main outcome |
|---|---|---|
| 04.1 | Existing Project Artifact Inspection | Verified repository inventory, dataset paths, and schemas |
| 04.2 | Real-Time Data Source Evaluation | Documented source selection and limitations |
| 04.3 | Live Weather Integration | Current weather and available forecast ingestion |
| 04.4 | Holiday and Festival Integration | Verified calendar dataset |
| 04.5 | Sports Event Integration | Validated sports-event records |
| 04.6 | Local Event Integration | Validated local-event records |
| 04.7 | Contextual Data Validation | Data-quality and provenance report |
| 04.8 | Historical Contextual Data Preparation | Historical contextual records where available |
| 04.9 | Zone-Aware Feature Preparation | Hourly and zone-aware contextual features |
| 04.10 | Historical Contextual Data Integration | Integrated historical research panel |
| 04.11 | Live Data Pipeline Integration | Refreshable contextual-data pipeline |
| 04.12 | Integration Testing and Validation | Test evidence and documented limitations |
| 04.13 | Phase 04 Documentation and Handover | Final summary and Phase 05 handover |

These are the proposed Phase 04 subsection names. During 04.1, compare them with the repository's existing conventions and adjust filenames/numbering only when needed.

## 11. Expected deliverables

- Source evaluation and provenance records
- Raw contextual data preserved separately from transformed data
- Validated weather, calendar, sports, and local-event datasets where available
- Historical contextual dataset(s) for retrospective evaluation where coverage permits
- A refreshable live contextual-data ingestion pipeline
- Zone-aware contextual features
- Integration and quality-check results
- Updated documentation and Phase 04 handover summary

## 12. Limitations

- Synthetic demand is not real customer-order data.
- Genuine contextual data does not establish causal effects on synthetic demand.
- Source coverage, resolution, licensing, and API availability must be verified.
- Local event listings may be incomplete or change after publication.
- Weather data may be forecast, observed, or modelled; these types must be distinguished.
- Real-world forecasting performance cannot be claimed without suitable real demand observations.

## 13. Phase status

**Status:** Not started. This document defines the planned scope only. No contextual data collection or integration should be considered complete until the relevant steps have been executed and validated.

**Next step:** Complete Step 04.1 — Existing Project Artifact Inspection using the actual repository and validated dataset files.
