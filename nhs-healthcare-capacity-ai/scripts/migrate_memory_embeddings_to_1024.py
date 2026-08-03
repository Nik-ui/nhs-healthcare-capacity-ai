import os

from dotenv import load_dotenv
import psycopg


load_dotenv()

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("DATABASE_URL is missing. Check your .env file.")

with psycopg.connect(database_url) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM memory_embeddings;")
        row_count = cur.fetchone()[0]

        if row_count:
            raise RuntimeError(
                "memory_embeddings already has rows. Stop here and review before changing dimensions."
            )

        cur.execute("DROP INDEX IF EXISTS memory_embeddings_embedding_idx;")
        cur.execute("DROP TABLE IF EXISTS memory_embeddings;")

        cur.execute(
            """
            CREATE TABLE memory_embeddings (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                memory_id UUID NOT NULL REFERENCES agent_memory (id) ON DELETE CASCADE,
                embedding VECTOR(1024),
                embedding_model STRING,
                created_at TIMESTAMPTZ NOT NULL DEFAULT now()
            );
            """
        )

        cur.execute(
            """
            CREATE VECTOR INDEX IF NOT EXISTS memory_embeddings_embedding_idx
            ON memory_embeddings (embedding vector_cosine_ops);
            """
        )

print("memory_embeddings migrated to VECTOR(1024).")
