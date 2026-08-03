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

CREATE TABLE IF NOT EXISTS beds_region_sector (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    period_date DATE NOT NULL,
    reporting_year STRING,
    period_end STRING,
    region_code STRING NOT NULL,
    region_name STRING NOT NULL,
    beds_available_total DECIMAL,
    ga_available DECIMAL,
    beds_occupied_total DECIMAL,
    ga_occupied DECIMAL,
    beds_occupancy_rate DECIMAL,
    ga_occupancy_rate DECIMAL,
    source_file STRING,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS ae_activity (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    period_date DATE NOT NULL,
    ae_type_1_attendances DECIMAL,
    ae_type_2_attendances DECIMAL,
    ae_type_3_attendances DECIMAL,
    ae_total_attendances DECIMAL,
    emergency_admissions_via_type_1_ae DECIMAL,
    emergency_admissions_via_type_2_ae DECIMAL,
    emergency_admissions_via_type_3_4_ae DECIMAL,
    emergency_admissions_via_ae DECIMAL,
    other_emergency_admissions DECIMAL,
    total_emergency_admissions DECIMAL,
    dta_waits_over_4h DECIMAL,
    dta_waits_over_12h DECIMAL,
    operational_standard DECIMAL,
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
    embedding VECTOR(1024),
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

CREATE INDEX IF NOT EXISTS beds_region_sector_period_region_idx
ON beds_region_sector (period_date, region_code);

CREATE UNIQUE INDEX IF NOT EXISTS beds_region_sector_unique_source_idx
ON beds_region_sector (period_date, region_code, source_file);

CREATE INDEX IF NOT EXISTS ae_activity_period_idx
ON ae_activity (period_date);

CREATE UNIQUE INDEX IF NOT EXISTS ae_activity_unique_source_idx
ON ae_activity (period_date, source_file);

CREATE INDEX IF NOT EXISTS agent_memory_created_at_idx
ON agent_memory (created_at DESC);

CREATE VECTOR INDEX IF NOT EXISTS memory_embeddings_embedding_idx
ON memory_embeddings (embedding vector_cosine_ops);
