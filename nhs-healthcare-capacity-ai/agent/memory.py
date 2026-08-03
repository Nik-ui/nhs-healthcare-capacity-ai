import os

from agent.db import connect
from agent.embeddings import generate_embedding, vector_to_sql


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


def save_memory_embedding(memory_id, text):
    embedding_model = os.getenv("EMBEDDING_MODEL", "amazon.titan-embed-text-v2:0")
    embedding = generate_embedding(text)
    embedding_sql = vector_to_sql(embedding)

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO memory_embeddings (
                    memory_id,
                    embedding,
                    embedding_model
                )
                VALUES (
                    %(memory_id)s,
                    %(embedding)s::VECTOR(1024),
                    %(embedding_model)s
                );
                """,
                {
                    "memory_id": memory_id,
                    "embedding": embedding_sql,
                    "embedding_model": embedding_model,
                },
            )


def save_memory_with_embedding(
    user_question,
    agent_answer,
    memory_summary,
    retrieved_context,
):
    memory_id = save_memory(
        user_question=user_question,
        agent_answer=agent_answer,
        memory_summary=memory_summary,
        retrieved_context=retrieved_context,
    )

    text_to_embed = (
        f"Question: {user_question}\n"
        f"Answer: {agent_answer}\n"
        f"Summary: {memory_summary}"
    )
    save_memory_embedding(memory_id=memory_id, text=text_to_embed)

    return memory_id


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


def get_similar_memories(query, limit=3):
    query_embedding = generate_embedding(query)
    query_vector = vector_to_sql(query_embedding)

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    am.id,
                    am.user_question,
                    am.agent_answer,
                    am.memory_summary,
                    am.created_at,
                    me.embedding <=> %(query_vector)s::VECTOR(1024) AS cosine_distance
                FROM memory_embeddings AS me
                JOIN agent_memory AS am
                    ON am.id = me.memory_id
                ORDER BY me.embedding <=> %(query_vector)s::VECTOR(1024)
                LIMIT %(limit)s;
                """,
                {
                    "query_vector": query_vector,
                    "limit": limit,
                },
            )

            rows = cur.fetchall()

    return [
        {
            "id": str(row[0]),
            "user_question": row[1],
            "agent_answer": row[2],
            "memory_summary": row[3],
            "created_at": str(row[4]),
            "cosine_distance": str(row[5]),
        }
        for row in rows
    ]
