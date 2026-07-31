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
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cur.fetchall()

print("Tables in CockroachDB:")
for table in tables:
    print(f"- {table[0]}")