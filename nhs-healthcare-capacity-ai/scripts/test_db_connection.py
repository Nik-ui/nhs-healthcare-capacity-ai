from dotenv import load_dotenv
import os
import psycopg


load_dotenv()

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("DATABASE_URL is missing. Check your .env file.")

with psycopg.connect(database_url) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]
        print("Connected to CockroachDB successfully.")
        print(version)