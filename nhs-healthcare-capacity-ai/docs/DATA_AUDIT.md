# Data Audit

## Repository Baseline

The original project files were found in:

`C:\Users\folah\my_python_projects`

They have been copied into a dedicated project workspace:

`C:\Users\folah\my_python_projects\nhs-healthcare-capacity-ai`

Original files copied:

- `notebooks/NHSDATA_original.ipynb`
- `data/raw/Beds-Open-Overnight-Web_File-Q3-2025-26_duplicate.xlsx`
- `data/raw/Monthly-AE-Time-Series-January-2026-C86cfU_duplicate.xls`

## Original Notebook

Notebook: `notebooks/NHSDATA_original.ipynb`

Audit result:

- 21 cells
- Only one `pd.read_excel(...)` call found
- The notebook loads the bed occupancy workbook only
- The A&E workbook is present in the original project but is not integrated in the notebook

Executed data load found:

```python
beds = pd.read_excel(
    "Beds-Open-Overnight-Web_File-Q3-2025-26_duplicate.xlsx",
    sheet_name="Region by Sector",
    header=14
)
```

## Bed Occupancy Workbook

File:

`data/raw/Beds-Open-Overnight-Web_File-Q3-2025-26_duplicate.xlsx`

Workbook audit:

- Sheets: `Region by Sector`
- Data shape with `header=14`: 9 rows, 22 columns
- Reporting period in metadata: October to December 2025
- Published in metadata: 19th February 2026
- Source in metadata: NHS England SDCS data collection - KH03

Key columns:

- `Year`
- `Period End`
- `Region Code`
- `AT Name`
- `Total `
- `General & Acute`
- `General & Acute.1`
- `General & Acute.2`

Column interpretation:

- `General & Acute`: available General and Acute beds
- `General & Acute.1`: occupied General and Acute beds
- `General & Acute.2`: General and Acute occupancy rate

## A&E Workbook

File:

`data/raw/Monthly-AE-Time-Series-January-2026-C86cfU_duplicate.xls`

Workbook audit:

- Sheets: `Activity`, `Chart Data`, `Charts`
- The useful source table appears on `Activity`
- Header row appears around row 14 in the raw workbook view
- Reporting period in metadata: August 2010 - present
- Published in metadata: 12th February 2026
- Source in metadata: Unify2 / SDCS data collections - WSitAE and MSitAE

Important fields visible in `Activity`:

- `Period`
- `Type 1 Departments - Major A&E`
- `Type 2 Departments - Single Specialty`
- `Type 3 Departments - Other A&E/Minor Injury Unit`
- `Total Attendances`
- `Emergency Admissions via Type 1 A&E`
- `Emergency Admissions via Type 2 A&E`
- `Emergency Admissions via Type 3 and 4 A&E`
- `Total Emergency Admissions via A&E`
- `Other Emergency Admissions (i.e not via A&E)`
- `Total Emergency Admissions`
- `Number of patients spending >4 hours from decision to admit to admission`
- `Number of patients spending >12 hours from decision to admit to admission`

## Immediate Data Work

Completed first-pass data task:

1. Built `scripts/prepare_data.py`.
2. Loaded the beds workbook from `data/raw`.
3. Loaded the A&E workbook from `data/raw`, sheet `Activity`.
4. Cleaned headers and removed metadata rows.
5. Produced cleaner project files in `data/processed`.
6. Created a prototype pressure score.

## Processed Outputs

Files created:

- `data/processed/beds_region_sector_clean.csv`
- `data/processed/beds_region_sector_clean.json`
- `data/processed/ae_activity_clean.csv`
- `data/processed/ae_activity_clean.json`
- `data/processed/national_capacity_pressure.csv`
- `data/processed/national_capacity_pressure.json`
- `data/processed/data_summary.json`

Summary:

- Bed rows: 8
- A&E monthly rows: 186
- Common merged national pressure rows: 1
- Bed period: December 2025
- A&E period range: August 2010 to January 2026
- Latest common period: December 2025

First merged pressure output:

- General and Acute occupancy rate: 0.9147
- A&E total attendances: 2,327,015
- Emergency admissions via A&E: 405,378
- Decision-to-admit waits over 12 hours: 50,775
- Prototype capacity pressure score: 64.8
- Prototype risk band: elevated

Important limitation:

The bed occupancy workbook only provides the Q3 2025-26 period ending December 2025, while the A&E workbook is a monthly time series. This means the first merged product view has one common month. A fuller dashboard trend will need either the NHS bed time series file or multiple quarterly bed files.
