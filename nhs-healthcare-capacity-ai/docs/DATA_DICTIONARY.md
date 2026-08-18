# Data Dictionary

This document explains the processed datasets used by NHS Capacity Memory Agent.

The project keeps raw NHS Excel workbooks in `data/raw` and creates cleaner files in `data/processed`.

## Why A Data Dictionary Matters

A data dictionary answers four questions:

- What does each column mean?
- Where did the data come from?
- How was the value calculated or cleaned?
- Why does it matter for the product?

This is useful because every answer, forecast, and product signal should have a clear source.

## Processed Files

| File | Purpose |
|---|---|
| `beds_region_sector_clean.csv` | Cleaned regional bed availability and occupancy data |
| `ae_activity_clean.csv` | Cleaned England-level monthly A&E activity data |
| `national_capacity_pressure.csv` | Merged national-level product dataset used for the pressure score |
| `data_summary.json` | Small metadata summary of row counts and date coverage |

JSON versions of the processed datasets are also created for future interface work.

## `beds_region_sector_clean`

Source file:

`data/raw/Beds-Open-Overnight-Web_File-Q3-2025-26_duplicate.xlsx`

Source sheet:

`Region by Sector`

| Column | Type | Meaning | Product Use |
|---|---|---|---|
| `period_date` | date | First day of the reporting month derived from the workbook period | Used for merging, filtering, and date-based questions |
| `reporting_year` | text | NHS reporting year, e.g. `2025-26` | Shows the official reporting year |
| `period_end` | text | Reporting period label, e.g. `December` | Human-readable period display |
| `region_code` | text | NHS region code; England total is set to `ENG` | Regional filtering and comparison |
| `region_name` | text | Region name, standardised to uppercase | Region labels in answers and comparisons |
| `beds_available_total` | number | Total beds available across bed sectors | Overall capacity signal |
| `ga_available` | number | General and Acute beds available | Main acute capacity signal |
| `beds_occupied_total` | number | Total occupied beds across bed sectors | Overall pressure signal |
| `ga_occupied` | number | General and Acute beds occupied | Main acute occupancy signal |
| `beds_occupancy_rate` | decimal | Total occupied beds divided by total available beds | Overall occupancy signal |
| `ga_occupancy_rate` | decimal | General and Acute occupied beds divided by General and Acute available beds | Primary bed pressure signal |

## `ae_activity_clean`

Source file:

`data/raw/Monthly-AE-Time-Series-January-2026-C86cfU_duplicate.xls`

Source sheet:

`Activity`

| Column | Type | Meaning | Product Use |
|---|---|---|---|
| `period_date` | date | Month of reported A&E activity | Trend and merge key |
| `ae_type_1_attendances` | number | Attendances at Type 1 Major A&E departments | Major emergency demand signal |
| `ae_type_2_attendances` | number | Attendances at Type 2 single-specialty departments | Specialist emergency demand signal |
| `ae_type_3_attendances` | number | Attendances at Type 3 minor injury / other A&E units | Urgent care demand signal |
| `ae_total_attendances` | number | Total A&E attendances across department types | Main demand KPI |
| `emergency_admissions_via_type_1_ae` | number | Emergency admissions via Type 1 A&E | Major A&E conversion to admission |
| `emergency_admissions_via_type_2_ae` | number | Emergency admissions via Type 2 A&E | Specialist A&E conversion to admission |
| `emergency_admissions_via_type_3_4_ae` | number | Emergency admissions via Type 3 and Type 4 A&E | Minor / other A&E admission signal |
| `emergency_admissions_via_ae` | number | Total emergency admissions via A&E | Main admission pressure signal |
| `other_emergency_admissions` | number | Emergency admissions not via A&E | Wider urgent admission demand |
| `total_emergency_admissions` | number | Total emergency admissions from all routes | Overall emergency admission KPI |
| `dta_waits_over_4h` | number | Patients waiting over 4 hours from decision to admit to admission | Flow delay signal |
| `dta_waits_over_12h` | number | Patients waiting over 12 hours from decision to admit to admission | Severe flow delay signal |
| `operational_standard` | decimal | A&E operational standard value shown in the workbook | Benchmark reference |

## `national_capacity_pressure`

This file merges England-level bed occupancy with A&E activity for common periods.

Current limitation:

The bed workbook currently covers one reporting period ending December 2025. The A&E workbook covers August 2010 to January 2026. Because of this, the first merged dataset has one common national month: December 2025.

| Column | Type | Meaning | Product Use |
|---|---|---|---|
| all bed columns | mixed | England-level fields from `beds_region_sector_clean` | Capacity side of the pressure view |
| all A&E columns | mixed | Monthly A&E fields from `ae_activity_clean` | Demand side of the pressure view |
| `admission_rate_via_ae` | decimal | `emergency_admissions_via_ae / ae_total_attendances` | Shows how much A&E demand converts into admissions |
| `dta_12h_wait_rate` | decimal | `dta_waits_over_12h / emergency_admissions_via_ae` | Shows severe waiting pressure relative to admissions |
| `capacity_pressure_score` | number | Prototype weighted score from occupancy, admission rate, and 12-hour wait rate | Main product pressure signal |
| `risk_band` | text | Label derived from the pressure score: `normal`, `elevated`, `high`, or `critical` | Simple status label used in the app |

## Prototype Pressure Score

The current pressure score is a product assumption, not an official NHS measure.

It combines three signals:

| Component | Weight | Why It Matters |
|---|---:|---|
| General and Acute occupancy rate | 55% | High acute occupancy reduces spare capacity |
| Admission rate via A&E | 25% | More A&E attendances turning into admissions increases bed demand |
| 12-hour decision-to-admit wait rate | 20% | Long waits indicate flow problems between emergency care and inpatient beds |

Risk bands:

| Score Range | Risk Band |
|---:|---|
| 0 to 54.9 | `normal` |
| 55 to 69.9 | `elevated` |
| 70 to 84.9 | `high` |
| 85 to 100 | `critical` |

## First Merged Output

For December 2025:

- General and Acute occupancy rate: 91.5%
- A&E total attendances: 2.33 million
- Emergency admissions via A&E: 405,378
- Decision-to-admit waits over 12 hours: 50,775
- Prototype pressure score: 64.8
- Risk band: `elevated`

## Important Limitation

The current pressure score is useful for product exploration, but it should be treated as a prototype. It needs validation with more historical bed data, clinical/operational input, and sensitivity testing before it could be used as a serious operational risk measure.
