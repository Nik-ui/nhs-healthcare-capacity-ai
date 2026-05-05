# NHS Capacity Intelligence Dashboard

AI-informed product prototype for identifying NHS emergency care capacity pressure using public NHS England data.

## Product Thesis

NHS operational teams need a fast way to understand when emergency demand and bed occupancy are creating capacity pressure. This project turns public NHS England datasets into a lightweight decision-support dashboard that surfaces pressure signals, trends, and risk bands.

## Current Stage

This repository is being rebuilt from an exploratory notebook into a product-focused healthtech case study:

- clean data analysis
- interactive dashboard prototype
- product research write-up
- product impact summary

## Data Sources

Raw files currently used or planned:

- `data/raw/Beds-Open-Overnight-Web_File-Q3-2025-26_duplicate.xlsx`
  - NHS England Bed Availability and Occupancy, Q3 2025-26
  - Sheet used: `Region by Sector`
  - Current notebook uses this file only
- `data/raw/Monthly-AE-Time-Series-January-2026-C86cfU_duplicate.xls`
  - NHS England Monthly A&E Attendances and Emergency Admissions, January 2026
  - Sheets available: `Activity`, `Chart Data`, `Charts`
  - Present in the original project but not yet integrated in the notebook

Official source pages:

- NHS England Bed Availability and Occupancy Data - Overnight: https://www.england.nhs.uk/statistics/statistical-work-areas/bed-availability-and-occupancy/bed-data-overnight/
- NHS England A&E Attendances and Emergency Admissions: https://www.england.nhs.uk/statistics/statistical-work-areas/ae-waiting-times-and-activity/

## Planned Product Outputs

- `notebooks/nhs_capacity_analysis.ipynb` - cleaned, reproducible analysis
- `scripts/prepare_data.py` - converts raw NHS files into dashboard-ready data
- `data/processed/` - CSV/JSON outputs for the dashboard
- `dashboard/` - fast React/Vite dashboard
- `docs/PRODUCT_RESEARCH_REPORT.md` - research and product strategy write-up
- `docs/PRODUCT_IMPACT_SUMMARY.md` - concise product impact and roadmap summary

## Core Product Metrics

The project will track:

- General and Acute bed occupancy rate
- General and Acute beds available
- General and Acute beds occupied
- A&E attendances
- emergency admissions
- waits over 4 hours from decision to admit
- waits over 12 hours from decision to admit
- capacity pressure score
- risk band: normal, elevated, high, critical

## Status

Baseline audit and first data integration complete.

The preparation script creates:

- `data/processed/beds_region_sector_clean.csv`
- `data/processed/beds_region_sector_clean.json`
- `data/processed/ae_activity_clean.csv`
- `data/processed/ae_activity_clean.json`
- `data/processed/national_capacity_pressure.csv`
- `data/processed/national_capacity_pressure.json`
- `data/processed/data_summary.json`

First merged national pressure row:

- Period: December 2025
- General and Acute occupancy: 91.5%
- A&E attendances: 2.33 million
- Emergency admissions via A&E: 405,378
- Decision-to-admit waits over 12 hours: 50,775
- Prototype pressure score: 64.8
- Prototype risk band: elevated

Next step: create the cleaned analysis notebook and data dictionary, then scaffold the React dashboard.
