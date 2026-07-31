from agent.db import connect


def save_memory(user_question, agent_answer, memory_summary, retrieved_context):
    with connect() as conn:
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

            return cur.fetchone()[0]


def get_recent_memories(limit=5):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    id,
                    user_question,
                    agent_answer,
                    memory_summary,
                    created_at
                FROM agent_memory
                ORDER BY created_at DESC
                LIMIT %(limit)s;
                """,
                {"limit": limit},
            )

            rows = cur.fetchall()

    return [
        {
            "id": str(row[0]),
            "user_question": row[1],
            "agent_answer": row[2],
            "memory_summary": row[3],
            "created_at": str(row[4]),
        }
        for row in rows
    ]