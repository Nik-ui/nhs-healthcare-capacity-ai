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
            DELETE FROM capacity_snapshots
            WHERE id NOT IN (
                SELECT min(id)
                FROM capacity_snapshots
                GROUP BY period_date, region_code, source_file
            );
        """)

        deleted_rows = cur.rowcount

print(f"Removed {deleted_rows} duplicate capacity snapshot row(s).")