from dotenv import load_dotenv
import os

import psycopg


load_dotenv()

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("DATABASE_URL is missing. Check your .env file.")


with psycopg.connect(database_url) as conn:
    with conn.cursor() as cur:
        print("Row counts in CockroachDB:")

        cur.execute("SELECT count(*) FROM capacity_snapshots;")
        print(f"capacity_snapshots: {cur.fetchone()[0]}")

        cur.execute("SELECT count(*) FROM beds_region_sector;")
        print(f"beds_region_sector: {cur.fetchone()[0]}")

        cur.execute("SELECT count(*) FROM ae_activity;")
        print(f"ae_activity: {cur.fetchone()[0]}")

        print()
        print("Capacity snapshots:")
        cur.execute("""
            SELECT
                period_date,
                region_name,
                ga_occupancy_rate,
                ae_total_attendances,
                emergency_admissions_via_ae,
                capacity_pressure_score,
                risk_band
            FROM capacity_snapshots
            ORDER BY created_at DESC
            LIMIT 10;
        """)

        for row in cur.fetchall():
            print(row)

        print()
        print("Beds region sector:")
        cur.execute("""
            SELECT
                period_date,
                region_code,
                region_name,
                ga_available,
                ga_occupied,
                ga_occupancy_rate
            FROM beds_region_sector
            ORDER BY region_name
            LIMIT 10;
        """)

        for row in cur.fetchall():
            print(row)

        print()
        print("A&E activity:")
        cur.execute("""
            SELECT
                period_date,
                ae_total_attendances,
                emergency_admissions_via_ae,
                dta_waits_over_4h,
                dta_waits_over_12h,
                operational_standard
            FROM ae_activity
            ORDER BY period_date DESC
            LIMIT 10;
        """)

        for row in cur.fetchall():
            print(row)