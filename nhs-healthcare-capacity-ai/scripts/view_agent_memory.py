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
                id,
                user_question,
                agent_answer,
                memory_summary,
                created_at
            FROM agent_memory
            ORDER BY created_at DESC;
        """)
        rows = cur.fetchall()

print("Agent memories in CockroachDB:")

for row in rows:
    print("----")
    print(f"ID: {row[0]}")
    print(f"Question: {row[1]}")
    print(f"Answer: {row[2]}")
    print(f"Summary: {row[3]}")
    print(f"Created at: {row[4]}")