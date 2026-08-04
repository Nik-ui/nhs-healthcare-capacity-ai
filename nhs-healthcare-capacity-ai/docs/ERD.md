# NHS Capacity Memory Agent ERD

This document shows how the CockroachDB tables relate to each other. It uses the industry-friendly crow's foot ERD style through Mermaid, which is easier to read in GitHub than the older academic Chen notation.

## Entity Relationship Diagram

```mermaid
erDiagram
    capacity_snapshots {
        UUID id PK
        DATE period_date
        STRING region_code
        STRING region_name
        DECIMAL ga_available
        DECIMAL ga_occupied
        DECIMAL ga_occupancy_rate
        DECIMAL ae_total_attendances
        DECIMAL emergency_admissions_via_ae
        DECIMAL dta_waits_over_12h
        DECIMAL capacity_pressure_score
        STRING risk_band
        STRING source_file
        TIMESTAMPTZ created_at
    }

    beds_region_sector {
        UUID id PK
        DATE period_date
        STRING reporting_year
        STRING period_end
        STRING region_code
        STRING region_name
        DECIMAL beds_available_total
        DECIMAL ga_available
        DECIMAL beds_occupied_total
        DECIMAL ga_occupied
        DECIMAL beds_occupancy_rate
        DECIMAL ga_occupancy_rate
        STRING source_file
        TIMESTAMPTZ created_at
    }

    ae_activity {
        UUID id PK
        DATE period_date
        DECIMAL ae_type_1_attendances
        DECIMAL ae_type_2_attendances
        DECIMAL ae_type_3_attendances
        DECIMAL ae_total_attendances
        DECIMAL emergency_admissions_via_type_1_ae
        DECIMAL emergency_admissions_via_type_2_ae
        DECIMAL emergency_admissions_via_type_3_4_ae
        DECIMAL emergency_admissions_via_ae
        DECIMAL other_emergency_admissions
        DECIMAL total_emergency_admissions
        DECIMAL dta_waits_over_4h
        DECIMAL dta_waits_over_12h
        DECIMAL operational_standard
        STRING source_file
        TIMESTAMPTZ created_at
    }

    agent_memory {
        UUID id PK
        STRING user_question
        STRING agent_answer
        STRING memory_summary
        STRING retrieved_context
        TIMESTAMPTZ created_at
    }

    memory_embeddings {
        UUID id PK
        UUID memory_id FK
        VECTOR embedding
        STRING embedding_model
        TIMESTAMPTZ created_at
    }

    recommendations {
        UUID id PK
        UUID snapshot_id FK
        UUID memory_id FK
        STRING recommendation_text
        STRING priority
        TIMESTAMPTZ created_at
    }

    agent_memory ||--o{ memory_embeddings : "has vector embedding"
    capacity_snapshots ||--o{ recommendations : "can generate"
    agent_memory ||--o{ recommendations : "can support"
```

## Simple Explanation

`capacity_snapshots` stores the high-level national capacity pressure view.

`beds_region_sector` stores regional General and Acute bed pressure, so the agent can answer questions like which region has the highest occupancy.

`ae_activity` stores monthly A&E attendances, admissions, and delay-to-admission waits, so the agent can answer trend questions.

`agent_memory` stores what users asked and what the agent answered.

`memory_embeddings` stores vector versions of memories. This allows semantic memory search, meaning the agent can find related memories even when the wording is different.

`recommendations` stores operational recommendations produced from NHS pressure signals and agent context.

## Relationship Notes

`memory_embeddings.memory_id` links each embedding back to one row in `agent_memory`.

`recommendations.snapshot_id` can link a recommendation to a capacity snapshot.

`recommendations.memory_id` can link a recommendation to the conversation memory that helped produce it.

The NHS data tables are not directly joined with foreign keys because the source files are monthly summary datasets. They are connected analytically through fields like `period_date`, `region_code`, and `region_name`.
