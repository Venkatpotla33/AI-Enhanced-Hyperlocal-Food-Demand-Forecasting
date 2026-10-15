# Phase 03 — Data Quality & Exploratory Analysis: Final Summary

## 1. Objective

Phase 03 examines the quality, structure, temporal behaviour, and demand characteristics of the synthetic food-order dataset created in Phase 02. The objective is to establish a validated hourly, zone-level demand series and document findings that can guide contextual data integration, feature engineering, forecasting, and model evaluation.

The notebook covers dataset profiling, transaction and order-value characteristics, meal periods, weekday/weekend differences, hourly and day-of-week patterns, weekly and monthly trends, zone-level demand and variability, autocorrelation, stationarity, seasonal decomposition, structural-break investigations, annual-pattern analysis, and forecasting-readiness validation.

## 2. Dataset and Analysis Coverage

The source transaction dataset contains **17,188,957 synthetic orders**, involving **50,000 synthetic customers**, **220 synthetic restaurants**, and five synthetic delivery zones in Hyderabad.

| Property | Result |
|---|---:|
| Source transactions | 17,188,957 |
| Source columns | 14 |
| Synthetic customers | 50,000 |
| Synthetic restaurants | 220 |
| Delivery zones | 5 |
| Source date coverage | January 2023–August 2026 |
| Complete daily observations | 1,338 days |
| Complete daily zone-level observations | 6,690 rows |
| Complete-date hourly zone-level observations | 160,560 rows |
| Hourly observations per zone | 32,112 |

The zones are Z01–Kondapur, Z02–Hitech City, Z03–Gachibowli, Z04–Madhapur, and Z05–Kukatpally.

The daily and hourly analyses use complete dates through **August 30, 2026**. The source contains some transactions on August 31, 2026, but not a complete day of observations. Therefore, August 31 is excluded from the complete-date hourly panel rather than treating unobserved hours as zero demand.

## 3. Transaction-Level Data Quality

The final transaction-quality audit checked missing values across the source columns, duplicate order IDs, order-value validity, timestamp validity, project date boundaries, zone identifiers, and consistency of stored temporal columns.

The audit results were:

- No missing values across the 14 source columns.
- No duplicate order IDs identified.
- No invalid order values identified by the implemented validity check.
- No invalid or missing timestamps identified.
- No transactions outside the defined project date range.
- No unexpected zone identifiers; all five expected zones were present.
- No mismatches between `order_year` and the year derived from `order_timestamp`.
- No mismatches between `order_month` and the year-month derived from `order_timestamp`, after comparing equivalent representations.

The first temporal-column comparison incorrectly compared a stored string such as `2023-01` with an integer month such as `1`. The corrected check compared the stored year-month string with the timestamp-derived `%Y-%m` value and returned zero mismatches. This was a validation-representation issue, not a data correction.

## 4. Overall Order and Order-Value Characteristics

The mean order value is **₹318.65**, the median is **₹313.55**, and the middle 50% of order values lie between **₹258.43 and ₹372.96**. The standard deviation is **₹81.83**, and the observed range is **₹93.83–₹688.34**.

The order-value distribution is positively skewed, with most transactions concentrated around ₹250–₹400 and a longer upper tail. Some observations lie beyond the upper box-plot whisker. They were retained because statistical extremeness alone does not prove that a record is invalid.

### Meal periods

| Meal period | Share of transactions |
|---|---:|
| Dinner | 25.30% |
| Lunch | 22.75% |
| Evening | 12.90% |
| Late Morning | 11.50% |
| Afternoon | 10.72% |
| Morning | 7.99% |

Lunch and dinner together account for approximately **48.05%** of transactions. This is evidence of strong intraday demand concentration in the synthetic dataset.

### Weekday and weekend

Weekdays account for 68.17% of total transactions and weekends for 31.83%. Because a typical week has five weekdays and two weekend days, average daily volume is the more informative comparison:

- Weekday average: approximately **12,556.52 orders per day**.
- Weekend average: approximately **14,286.48 orders per day**.
- Average daily weekend demand is approximately **13.8% higher** than weekday demand.

Saturday has the highest transaction volume among the days of the week, while Monday has the lowest. Average order values remain relatively stable across weekdays, indicating that the observed day-of-week differences primarily concern order volume.

## 5. Hourly and Intraday Demand Patterns

The source transaction analysis identifies a pronounced 24-hour demand cycle.

| Measure | Finding |
|---|---|
| Highest-demand hour | 21:00 |
| Orders at 21:00 | 1,623,592 |
| Share of all transactions at 21:00 | Approximately 9.50% |
| Lowest-demand hour | 03:00 |
| Orders at 03:00 | 134,731 |
| Share of all transactions at 03:00 | Approximately 0.78% |

Demand is low during the early morning, increases through the morning, rises around lunch (particularly 12:00–14:00), falls during the afternoon, and increases again during the evening. The strongest peak occurs around dinner time at 21:00.

All five zones and both day types reach their highest hourly volume at 21:00. The lowest hour is generally 03:00 or 04:00, depending on the zone or day type. The common timing of the peaks indicates a shared intraday pattern, while the absolute demand levels differ across zones.

These findings support preserving hourly resolution in the forecasting target and evaluating hour-of-day, meal-period, and day-type information as candidate predictors in Phase 05.

## 6. Day-of-Week, Weekly, Monthly, and Quarterly Patterns

### Day of week

Saturday records **2,901,524 orders (16.88%)**, the highest day-of-week total. Monday records **2,088,902 orders (12.15%)**, the lowest. The normalized day-of-week distribution is similar across zones: Saturday contributes approximately 16.85%–16.90% of each zone's orders, while Monday contributes approximately 12.14%–12.17%.

The analysis shows a recurring weekly pattern in the generated data. These results should not be interpreted as verified real-world Hyderabad demand behaviour.

### Weekly demand

The weekly analysis contains 193 calendar-week periods, including 191 complete weeks and two partial weeks at the study boundaries. Partial weeks should not be compared directly with complete weeks without accounting for their different numbers of observed days.

### Monthly and quarterly demand

The monthly analysis covers 44 calendar months, from January 2023 through August 2026. The notebook reports that December 2023 had the highest monthly total, with **457,943 orders**, while February 2026 had the lowest monthly total, with **348,284 orders**. Monthly totals must be interpreted alongside month length and data coverage.

December 2023 had the highest reported average daily demand, approximately **14,772.35 orders per day**; May 2023 had the lowest, approximately **11,599.71 orders per day**. The quarterly comparison found the highest average daily demand in Q4 (approximately 14,196 orders) and the lowest in Q2 (approximately 12,214 orders). The 2026 third quarter is incomplete and should not be compared with a complete quarter by total volume.

### Recurring May demand dip

The annual-pattern investigation found that May had the lowest normalized monthly demand index in each of the three complete calendar years:

| Year | May normalized demand index |
|---|---:|
| 2023 | 89.63 |
| 2024 | 90.59 |
| 2025 | 91.17 |

The April–May–June comparison also found May's average daily demand below both April and June in all 20 year-zone combinations examined. This is a repeatable pattern in the current synthetic dataset, but its cause has not been established. It must not be presented as confirmed real-world seasonality.

## 7. Zone-Level Demand and Variability

### Overall contribution

| Zone | Share of all transactions |
|---|---:|
| Z02 — Hitech City | 24.74% |
| Z03 — Gachibowli | 22.75% |
| Z05 — Kukatpally | 18.67% |
| Z04 — Madhapur | 18.20% |
| Z01 — Kondapur | 15.65% |

Z02 contributes the most orders, followed by Z03; Z01 contributes the least.

### Daily zone-level demand

The daily zone-level analysis contains 1,338 complete daily observations per zone.

| Zone | Mean daily orders | Median daily orders | Standard deviation |
|---|---:|---:|---:|
| Z01 | 2,010.58 | 1,987.00 | 250.83 |
| Z02 | 3,176.65 | 3,140.50 | 394.32 |
| Z03 | 2,923.03 | 2,887.50 | 363.39 |
| Z04 | 2,337.65 | 2,313.50 | 291.39 |
| Z05 | 2,398.75 | 2,368.00 | 300.63 |

Z02 has the highest average daily demand and absolute standard deviation, while Z01 has the lowest. The mean exceeds the median in every zone, and the daily distributions show positive skewness. The notebook's Shapiro–Wilk tests reject normality for all five zone-level daily distributions at the 5% significance level.

Absolute and relative variability are not identical. Z02 has the largest absolute fluctuations, while Z05 has the highest reported coefficient of variation (approximately 12.53%) and Z02 the lowest (approximately 12.41%). This distinction should be considered when selecting and interpreting scale-dependent forecasting metrics.

### Potential outliers and high-demand observations

The zone-level outlier analysis identified 23 statistical potential outliers: Z03 (7), Z04 (7), Z02 (4), Z01 (3), and Z05 (2). A separate daily volatility analysis flagged 67 days using the 95th percentile of absolute day-to-day percentage changes (approximately 18.57%).

These are exploratory flags, not confirmed demand surges or data errors. Contextual evidence and model evaluation are needed before assigning operational meaning to them.

### Cross-zone relationships

The daily zone-level demand correlations range approximately from **0.977 to 0.980**. The strongest reported pair is Z02–Z03 (approximately 0.980), and the weakest is Z01–Z05 (approximately 0.977). The hourly demand series also have pairwise correlations of approximately 0.98.

The zones therefore have different demand magnitudes but highly similar temporal patterns in this synthetic dataset. This supports comparing zone-specific and shared/global forecasting approaches later; correlation alone does not establish which approach will perform better.

## 8. Time-Series Diagnostics

### Autocorrelation and lag relationships

Daily demand has positive one-day lag correlations of approximately 0.60 across zones. Two-day lag correlations are close to zero, and three-day lag correlations are negative (approximately -0.226 to -0.216).

The seven-day lag correlations are approximately 0.949–0.954. Fourteen-day correlations are approximately 0.922–0.924, and 28-day correlations are approximately 0.865. This is strong evidence of recurring weekly dependence in the synthetic daily series.

Lag-1, lag-7, lag-14, and lag-28 demand are candidate features for later experiments, but their value must be assessed using chronological validation to prevent future information from leaking into training features.

### Daily stationarity and decomposition

For the 1,338-observation daily demand series, the Augmented Dickey–Fuller test reported:

- ADF statistic: **-3.680377**
- p-value: **0.00439779**
- Lags used: 23
- Observations used: 1,314

At the 5% significance level, the unit-root null hypothesis is rejected for the tested daily series. This does not rule out seasonal structure or every other form of non-stationarity.

The seven-day additive decomposition identifies a strong weekly component. Saturday has the largest positive seasonal effect (approximately +2,343.07 orders), and Monday has the strongest negative effect (approximately -1,908.70 orders). The trend and residual components capture changes not explained by the estimated weekly pattern. The notebook notes pronounced changes near the beginning of calendar years, whose cause remains unresolved.

### Weekly decomposition, differencing, and residual diagnostics

The notebook also investigates weekly demand using a 52-week seasonal period, including trend/seasonal/residual decomposition, seasonal and trend strength, residual autocorrelation (Ljung–Box testing), and 52-week seasonal differencing with ADF/KPSS diagnostics.

These analyses provide diagnostic evidence for candidate statistical model specifications. They do not, by themselves, determine the best model or prove that a particular transformation will improve forecast accuracy. That decision belongs to model evaluation and rolling-origin backtesting.

### Structural breaks and large changes

The notebook investigates potential change points and their sensitivity to penalty settings across zones. Detected change points and large daily changes identify periods for further examination; they do not establish the cause of a change or prove that it represents a real operational surge.

## 9. Final Hourly Panel and Forecasting-Readiness Validation

The corrected hourly demand panel was constructed from transactions on complete dates only, through August 30, 2026.

| Validation | Result |
|---|---:|
| Hourly zone-level records | 160,560 |
| Zones | 5 |
| Hours per zone | 32,112 |
| Duplicate zone-hour combinations | 0 |
| Missing hourly intervals | 0 |
| Missing required values | 0 |
| Negative hourly demand values | 0 |
| Transaction-to-hourly reconciliation | Passed |

The panel spans January 1, 2023, 00:00 through August 30, 2026, 23:00. The initial validation that expected a complete August 31 identified 120 missing zone-hour combinations. Subsequent investigation established that August 31 contains transactions only during its first hour. The incomplete date was therefore excluded from the complete-date panel, rather than filling its unobserved hours with zeros.

The initial diagnostic is retained for traceability, and the corrected panel validation supersedes the initial missing-combination result.

## 10. Implications for Subsequent Phases

The findings from Phase 03 inform the next phases as follows:

- **Phase 04 — Contextual Data Collection & Integration:** preserve the validated timestamp and zone keys; integrate weather, public holidays, and IPL schedules with appropriate temporal alignment.
- **Phase 05 — Feature Engineering:** investigate hour-of-day, meal period, day of week, weekend indicator, calendar features, and lagged demand, while ensuring that all predictors use information available at forecast time.
- **Phase 06 — Forecasting Models:** compare appropriate statistical, machine-learning/deep-learning, and time-series foundation-model approaches using the same target definition and data boundaries.
- **Phase 07 — Model Evaluation & Backtesting:** use chronological splits and rolling-origin evaluation; compare results by zone and forecast horizon, and assess whether contextual information improves performance.
- **Phase 08 — AI Surge Intelligence Layer:** distinguish statistically high demand from genuinely useful surge alerts using forecast errors, thresholds, and eventually contextual evidence.
- **Phases 09–10 — Power BI and Streamlit:** use consistent zone, timestamp, forecast, and evaluation definitions when presenting results.
- **Phases 11–12 — Research Conclusions and Documentation:** report findings as results from a synthetic proxy dataset and clearly separate exploratory observations from conclusions supported by backtesting.

## 11. Limitations

1. **Synthetic data:** Demand volumes, zone differences, seasonal patterns, and cross-zone correlations are characteristics of the generated dataset and are not validated measurements of actual Hyderabad food-delivery activity.
2. **Potential generation effects:** The very similar temporal profiles across zones and the repeated May decline may partly reflect the synthetic generation process. Their causes have not been established in Phase 03.
3. **Contextual variables not yet integrated:** Weather, public holidays, and IPL schedules are planned for Phase 04 and are not yet available to explain observed patterns.
4. **Incomplete final date:** August 31, 2026, is excluded from the complete-date hourly panel. The forecasting dataset's date boundary must remain consistent in later phases.
5. **Outlier interpretation:** Statistical outliers, large daily changes, and detected change points are not automatically data errors or confirmed surges.
6. **Exploratory evidence is not predictive proof:** Candidate features and model choices must be assessed with chronological validation and rolling-origin backtesting.

## 12. Conclusion and Phase 03 Status

Phase 03 established the quality and structure of the transaction dataset, validated the corrected complete-date hourly demand panel, and documented the main temporal and zone-level characteristics of the synthetic demand series. The notebook investigated intraday and weekly patterns, monthly and annual variation, order-value distributions, zone-level demand and variability, autocorrelation, stationarity, seasonal decomposition, and potential structural changes.

The final transaction audit passed the checks performed, including missing values, duplicate IDs, order-value validity, timestamps, zone identifiers, and temporal-column consistency. The corrected hourly panel contains 160,560 observations across five zones, has continuous hourly coverage over the validated date range, and reconciles with the complete-date transaction source.

The most relevant findings are the strong dinner peak at 21:00, higher average daily weekend demand, pronounced weekly dependence, different demand magnitudes but highly similar temporal profiles across zones, and a recurring May demand dip in the synthetic dataset. These observations guide later experiments but are not assumed to represent real-world market behaviour or to guarantee predictive value.

**Phase 03 is ready to close once this summary and the incomplete-final-date validation note are saved in the notebook and the final notebook is reviewed.** The next planned phase is **Phase 04 — Contextual Data Collection & Integration**. No additional general EDA is recommended unless a specific unresolved data-quality issue emerges.
