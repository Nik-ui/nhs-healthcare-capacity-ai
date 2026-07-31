from dotenv import load_dotenv
import csv
import os
from pathlib import Path

import psycopg


load_dotenv()

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("DATABASE_URL is missing. Check your .env file.")

csv_path = Path("data/processed/national_capacity_pressure.csv")

if not csv_path.exists():
    raise FileNotFoundError(f"Could not find {csv_path}")

rows_loaded = 0

with psycopg.connect(database_url) as conn:
    with conn.cursor() as cur:
        with csv_path.open("r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                cur.execute(
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
                        "ga_available": row["ga_available"],
                        "ga_occupied": row["ga_occupied"],
                        "ga_occupancy_rate": row["ga_occupancy_rate"],
                        "ae_total_attendances": row["ae_total_attendances"],
                        "emergency_admissions_via_ae": row["emergency_admissions_via_ae"],
                        "dta_waits_over_12h": row["dta_waits_over_12h"],
                        "capacity_pressure_score": row["capacity_pressure_score"],
                        "risk_band": row["risk_band"],
                        "source_file": "national_capacity_pressure.csv",
                    },
                )
                rows_loaded += 1

print(f"Loaded or updated {rows_loaded} capacity snapshot row(s).")