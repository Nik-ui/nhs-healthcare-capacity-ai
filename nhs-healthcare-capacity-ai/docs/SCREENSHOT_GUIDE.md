# Screenshot Guide

Save demo screenshots in:

```text
docs/demo_assets/
```

Recommended screenshots:

1. `01_homepage.png`
   - Shows the live product landing view.
   - Include the title, question box, current signals, and technology badges.

2. `02_capacity_answer.png`
   - Ask: `Which region has the highest bed occupancy?`
   - Capture the answer card.

3. `03_forecast_answer.png`
   - Ask: `What is the likely A&E pressure trend over the next 3 months?`
   - Capture the forecast answer.

4. `04_memory_recall.png`
   - Ask: `What did I ask earlier about capacity pressure?`
   - Capture the memory recall answer.

5. `05_api_docs.png`
   - Open: `https://nhs-healthcare-capacity-ai.vercel.app/docs`
   - Capture the FastAPI `/ask` endpoint.

6. `06_cockroach_tables.png`
   - Capture CockroachDB tables if available:
     - `capacity_snapshots`
     - `beds_region_sector`
     - `ae_activity`
     - `agent_memory`
     - `memory_embeddings`

7. `07_architecture.png`
   - Capture the architecture diagram from `docs/ARCHITECTURE.md`.

## Screenshot Notes

Do not show:

- `.env`
- AWS access keys
- database passwords
- Vercel environment variable values
- full CockroachDB connection strings

It is safe to show:

- table names
- app UI
- generated answers
- memory IDs
- API docs
- architecture diagrams
