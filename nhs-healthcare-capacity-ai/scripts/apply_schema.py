from dotenv import load_dotenv
import os
from pathlib import Path
import psycopg


load_dotenv()

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("DATABASE_URL is missing. Check your .env file.")

schema_path = Path("database/schema.sql")
schema_sql = schema_path.read_text(encoding="utf-8")

with psycopg.connect(database_url) as conn:
    with conn.cursor() as cur:
        cur.execute(schema_sql)

print("Database schema applied successfully.")