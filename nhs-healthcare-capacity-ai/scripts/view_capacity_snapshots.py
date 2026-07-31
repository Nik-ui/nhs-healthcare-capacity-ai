from dotenv import load_dotenv
import os
import psycopg


load_dotenv()

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("DATABASE_URL is missing. Check your .env file.")

with psycopg.connect(database_url) as conn:
    with conn.cursor() as cur:
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
            ORDER BY created_at DESC;
        """)
        rows = cur.fetchall()

print("Capacity snapshots in CockroachDB:")
for row in rows:
    print(row)