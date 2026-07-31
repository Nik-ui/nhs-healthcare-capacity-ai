-- NHS Capacity Memory Agent database schema

CREATE TABLE IF NOT EXISTS capacity_snapshots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    period_date DATE NOT NULL,
    region_code STRING NOT NULL,
    region_name STRING NOT NULL,
    ga_available DECIMAL,
    ga_occupied DECIMAL,
    ga_occupancy_rate DECIMAL,
    ae_total_attendances DECIMAL,
    emergency_admissions_via_ae DECIMAL,
    dta_waits_over_12h DECIMAL,
    capacity_pressure_score DECIMAL,
    risk_band STRING,
    source_file STRING,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS agent_memory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_question STRING NOT NULL,
    agent_answer STRING NOT NULL,
    memory_summary STRING,
    retrieved_context STRING,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS memory_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    memory_id UUID NOT NULL REFERENCES agent_memory (id) ON DELETE CASCADE,
    embedding VECTOR(1536),
    embedding_model STRING,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS recommendations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    snapshot_id UUID REFERENCES capacity_snapshots (id) ON DELETE SET NULL,
    memory_id UUID REFERENCES agent_memory (id) ON DELETE SET NULL,
    recommendation_text STRING NOT NULL,
    priority STRING,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS capacity_snapshots_period_region_idx
ON capacity_snapshots (period_date, region_code);

CREATE UNIQUE INDEX IF NOT EXISTS capacity_snapshots_unique_source_idx
ON capacity_snapshots (period_date, region_code, source_file);

CREATE INDEX IF NOT EXISTS agent_memory_created_at_idx
ON agent_memory (created_at DESC);

CREATE VECTOR INDEX IF NOT EXISTS memory_embeddings_embedding_idx
ON memory_embeddings (embedding);

