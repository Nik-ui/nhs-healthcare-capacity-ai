from dotenv import load_dotenv
import csv
import os
from pathlib import Path

import psycopg


load_dotenv()

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("DATABASE_URL is missing. Check your .env file.")


def clean_decimal(value):
    if value == "":
        return None

    return value


def load_capacity_snapshots(cursor):
    csv_path = Path("data/processed/national_capacity_pressure.csv")

    if not csv_path.exists():
        raise FileNotFoundError(f"Could not find {csv_path}")

    rows_loaded = 0

    with csv_path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            cursor.execute(
                """
                INSERT INTO capacity_snapshots (
                    period_date,
                    region_code,
                    region_name,
                    ga_available,
                    ga_occupied,
                    ga_occupancy_rate,
                    ae_total_attendances,
                    emergency_admissions_via_ae,
                    dta_waits_over_12h,
                    capacity_pressure_score,
                    risk_band,
                    source_file
                )
                VALUES (
                    %(period_date)s,
                    %(region_code)s,
                    %(region_name)s,
                    %(ga_available)s,
                    %(ga_occupied)s,
                    %(ga_occupancy_rate)s,
                    %(ae_total_attendances)s,
                    %(emergency_admissions_via_ae)s,
                    %(dta_waits_over_12h)s,
                    %(capacity_pressure_score)s,
                    %(risk_band)s,
                    %(source_file)s
                )
                ON CONFLICT (period_date, region_code, source_file)
                DO UPDATE SET
                    region_name = excluded.region_name,
                    ga_available = excluded.ga_available,
                    ga_occupied = excluded.ga_occupied,
                    ga_occupancy_rate = excluded.ga_occupancy_rate,
                    ae_total_attendances = excluded.ae_total_attendances,
                    emergency_admissions_via_ae = excluded.emergency_admissions_via_ae,
                    dta_waits_over_12h = excluded.dta_waits_over_12h,
                    capacity_pressure_score = excluded.capacity_pressure_score,
                    risk_band = excluded.risk_band;
                """,
                {
                    "period_date": row["period_date"],
                    "region_code": row["region_code"],
                    "region_name": row["region_name"],
                    "ga_available": clean_decimal(row["ga_available"]),
                    "ga_occupied": clean_decimal(row["ga_occupied"]),
                    "ga_occupancy_rate": clean_decimal(row["ga_occupancy_rate"]),
                    "ae_total_attendances": clean_decimal(row["ae_total_attendances"]),
                    "emergency_admissions_via_ae": clean_decimal(row["emergency_admissions_via_ae"]),
                    "dta_waits_over_12h": clean_decimal(row["dta_waits_over_12h"]),
                    "capacity_pressure_score": clean_decimal(row["capacity_pressure_score"]),
                    "risk_band": row["risk_band"],
                    "source_file": "national_capacity_pressure.csv",
                },
            )
            rows_loaded += 1

    return rows_loaded


def load_beds_region_sector(cursor):
    csv_path = Path("data/processed/beds_region_sector_clean.csv")

    if not csv_path.exists():
        raise FileNotFoundError(f"Could not find {csv_path}")

    rows_loaded = 0

    with csv_path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            cursor.execute(
                """
                INSERT INTO beds_region_sector (
                    period_date,
                    reporting_year,
                    period_end,
                    region_code,
                    region_name,
                    beds_available_total,
                    ga_available,
                    beds_occupied_total,
                    ga_occupied,
                    beds_occupancy_rate,
                    ga_occupancy_rate,
                    source_file
                )
                VALUES (
                    %(period_date)s,
                    %(reporting_year)s,
                    %(period_end)s,
                    %(region_code)s,
                    %(region_name)s,
                    %(beds_available_total)s,
                    %(ga_available)s,
                    %(beds_occupied_total)s,
                    %(ga_occupied)s,
                    %(beds_occupancy_rate)s,
                    %(ga_occupancy_rate)s,
                    %(source_file)s
                )
                ON CONFLICT (period_date, region_code, source_file)
                DO UPDATE SET
                    reporting_year = excluded.reporting_year,
                    period_end = excluded.period_end,
                    region_name = excluded.region_name,
                    beds_available_total = excluded.beds_available_total,
                    ga_available = excluded.ga_available,
                    beds_occupied_total = excluded.beds_occupied_total,
                    ga_occupied = excluded.ga_occupied,
                    beds_occupancy_rate = excluded.beds_occupancy_rate,
                    ga_occupancy_rate = excluded.ga_occupancy_rate;
                """,
                {
                    "period_date": row["period_date"],
                    "reporting_year": row["reporting_year"],
                    "period_end": row["period_end"],
                    "region_code": row["region_code"],
                    "region_name": row["region_name"],
                    "beds_available_total": clean_decimal(row["beds_available_total"]),
                    "ga_available": clean_decimal(row["ga_available"]),
                    "beds_occupied_total": clean_decimal(row["beds_occupied_total"]),
                    "ga_occupied": clean_decimal(row["ga_occupied"]),
                    "beds_occupancy_rate": clean_decimal(row["beds_occupancy_rate"]),
                    "ga_occupancy_rate": clean_decimal(row["ga_occupancy_rate"]),
                    "source_file": "beds_region_sector_clean.csv",
                },
            )
            rows_loaded += 1

    return rows_loaded


def load_ae_activity(cursor):
    csv_path = Path("data/processed/ae_activity_clean.csv")

    if not csv_path.exists():
        raise FileNotFoundError(f"Could not find {csv_path}")

    rows_loaded = 0

    with csv_path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            cursor.execute(
                """
                INSERT INTO ae_activity (
                    period_date,
                    ae_type_1_attendances,
                    ae_type_2_attendances,
                    ae_type_3_attendances,
                    ae_total_attendances,
                    emergency_admissions_via_type_1_ae,
                    emergency_admissions_via_type_2_ae,
                    emergency_admissions_via_type_3_4_ae,
                    emergency_admissions_via_ae,
                    other_emergency_admissions,
                    total_emergency_admissions,
                    dta_waits_over_4h,
                    dta_waits_over_12h,
                    operational_standard,
                    source_file
                )
                VALUES (
                    %(period_date)s,
                    %(ae_type_1_attendances)s,
                    %(ae_type_2_attendances)s,
                    %(ae_type_3_attendances)s,
                    %(ae_total_attendances)s,
                    %(emergency_admissions_via_type_1_ae)s,
                    %(emergency_admissions_via_type_2_ae)s,
                    %(emergency_admissions_via_type_3_4_ae)s,
                    %(emergency_admissions_via_ae)s,
                    %(other_emergency_admissions)s,
                    %(total_emergency_admissions)s,
                    %(dta_waits_over_4h)s,
                    %(dta_waits_over_12h)s,
                    %(operational_standard)s,
                    %(source_file)s
                )
                ON CONFLICT (period_date, source_file)
                DO UPDATE SET
                    ae_type_1_attendances = excluded.ae_type_1_attendances,
                    ae_type_2_attendances = excluded.ae_type_2_attendances,
                    ae_type_3_attendances = excluded.ae_type_3_attendances,
                    ae_total_attendances = excluded.ae_total_attendances,
                    emergency_admissions_via_type_1_ae = excluded.emergency_admissions_via_type_1_ae,
                    emergency_admissions_via_type_2_ae = excluded.emergency_admissions_via_type_2_ae,
                    emergency_admissions_via_type_3_4_ae = excluded.emergency_admissions_via_type_3_4_ae,
                    emergency_admissions_via_ae = excluded.emergency_admissions_via_ae,
                    other_emergency_admissions = excluded.other_emergency_admissions,
                    total_emergency_admissions = excluded.total_emergency_admissions,
                    dta_waits_over_4h = excluded.dta_waits_over_4h,
                    dta_waits_over_12h = excluded.dta_waits_over_12h,
                    operational_standard = excluded.operational_standard;
                """,
                {
                    "period_date": row["period_date"],
                    "ae_type_1_attendances": clean_decimal(row["ae_type_1_attendances"]),
                    "ae_type_2_attendances": clean_decimal(row["ae_type_2_attendances"]),
                    "ae_type_3_attendances": clean_decimal(row["ae_type_3_attendances"]),
                    "ae_total_attendances": clean_decimal(row["ae_total_attendances"]),
                    "emergency_admissions_via_type_1_ae": clean_decimal(row["emergency_admissions_via_type_1_ae"]),
                    "emergency_admissions_via_type_2_ae": clean_decimal(row["emergency_admissions_via_type_2_ae"]),
                    "emergency_admissions_via_type_3_4_ae": clean_decimal(row["emergency_admissions_via_type_3_4_ae"]),
                    "emergency_admissions_via_ae": clean_decimal(row["emergency_admissions_via_ae"]),
                    "other_emergency_admissions": clean_decimal(row["other_emergency_admissions"]),
                    "total_emergency_admissions": clean_decimal(row["total_emergency_admissions"]),
                    "dta_waits_over_4h": clean_decimal(row["dta_waits_over_4h"]),
                    "dta_waits_over_12h": clean_decimal(row["dta_waits_over_12h"]),
                    "operational_standard": clean_decimal(row["operational_standard"]),
                    "source_file": "ae_activity_clean.csv",
                },
            )
            rows_loaded += 1

    return rows_loaded


with psycopg.connect(database_url) as conn:
    with conn.cursor() as cur:
        capacity_rows = load_capacity_snapshots(cur)
        beds_rows = load_beds_region_sector(cur)
        ae_rows = load_ae_activity(cur)

print(f"Loaded or updated {capacity_rows} capacity snapshot row(s).")
print(f"Loaded or updated {beds_rows} bed region row(s).")
print(f"Loaded or updated {ae_rows} A&E activity row(s).")