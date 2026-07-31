from dotenv import load_dotenv
import os

import psycopg


load_dotenv()

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("DATABASE_URL is missing. Check your .env file.")

user_question = "What is the current NHS capacity risk for England?"
agent_answer = (
    "England is currently in the elevated risk band, with a capacity pressure "
    "score of 64.8 and General and Acute bed occupancy around 91.47%."
)
memory_summary = (
    "User asked about NHS capacity risk for England. The agent answered that "
    "England is elevated risk, with pressure score 64.8 and bed occupancy 91.47%."
)
retrieved_context = (
    "capacity_snapshots row: period_date=2025-12-01, region=ENGLAND, "
    "ga_occupancy_rate=0.914708909182848, capacity_pressure_score=64.8, "
    "risk_band=elevated"
)

with psycopg.connect(database_url) as conn:
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO agent_memory (
                user_question,
                agent_answer,
                memory_summary,
                retrieved_context
            )
            VALUES (
                %(user_question)s,
                %(agent_answer)s,
                %(memory_summary)s,
                %(retrieved_context)s
            )
            RETURNING id;
            """,
            {
                "user_question": user_question,
                "agent_answer": agent_answer,
                "memory_summary": memory_summary,
                "retrieved_context": retrieved_context,
            },
        )

        memory_id = cur.fetchone()[0]

print("Saved agent memory successfully.")
print(f"Memory ID: {memory_id}")