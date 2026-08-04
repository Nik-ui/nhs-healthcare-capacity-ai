# NHS Capacity Memory Agent Architecture

This document explains the deployed system from user question to saved memory.

## Production Flow

```mermaid
flowchart TD
    User[User opens Vercel app] --> UI[FastAPI web UI]
    UI --> AskAPI[POST /ask]
    AskAPI --> Orchestrator[Agent orchestrator]

    Orchestrator --> CapacityTool[Capacity summary tool]
    Orchestrator --> BedTool[Regional bed pressure tool]
    Orchestrator --> AETool[A&E history tool]
    Orchestrator --> ForecastTool[A&E forecast tool]
    Orchestrator --> RecentMemory[Recent memory retrieval]
    Orchestrator --> VectorMemory[Vector memory search]

    CapacityTool --> Cockroach[(CockroachDB Cloud)]
    BedTool --> Cockroach
    AETool --> Cockroach
    ForecastTool --> Cockroach
    RecentMemory --> Cockroach
    VectorMemory --> Cockroach

    VectorMemory --> SimilarContext[Similar previous questions]
    Cockroach --> StructuredContext[Structured NHS and memory context]
    SimilarContext --> Prompt[Prompt assembly]
    StructuredContext --> Prompt

    Prompt --> Bedrock[AWS Bedrock text model]
    Bedrock --> Answer[Operational answer]

    Answer --> SaveMemory[Save question and answer]
    SaveMemory --> Cockroach
    SaveMemory --> Embedding[Bedrock Titan embedding]
    Embedding --> VectorTable[memory_embeddings]
    VectorTable --> Cockroach

    Answer --> UI
```

## Components

`app/main.py`

FastAPI application. It serves the web UI, exposes `/health`, exposes `/signals`, and accepts user questions through `/ask`.

`app/static/index.html`

The deployed product interface. Users can ask capacity, A&E, forecast, and memory questions.

`agent/orchestrator.py`

Coordinates retrieval, forecasting, memory search, Bedrock answer generation, and memory saving.

`agent/tools.py`

Contains CockroachDB data tools for:

- national capacity summary
- regional bed pressure
- A&E activity history
- A&E time trend

`agent/forecasting.py`

Creates a simple 3-month A&E pressure forecast using recent monthly history.

`agent/memory.py`

Stores user questions and agent answers. It also retrieves recent memories and similar memories.

`agent/embeddings.py`

Creates Bedrock Titan vector embeddings and formats them for CockroachDB vector search.

`agent/bedrock_client.py`

Connects to AWS Bedrock for text generation and embedding generation.

`agent/db.py`

Connects to CockroachDB using private environment variables.

## Database Role

CockroachDB is the persistent intelligence layer.

It stores:

- capacity data
- regional bed pressure
- A&E activity
- agent memory
- vector embeddings
- recommendation-ready records

## Memory Flow

```mermaid
flowchart TD
    Question[User question] --> EmbedQuestion[Create query embedding]
    EmbedQuestion --> Search[Search memory_embeddings with cosine distance]
    Search --> PreviousMemory[Retrieve related previous memories]
    PreviousMemory --> Prompt[Add memory to prompt context]
    Prompt --> Bedrock[AWS Bedrock]
    Bedrock --> Answer[Answer]
    Answer --> Save[Save new memory]
    Save --> NewEmbedding[Create answer embedding]
    NewEmbedding --> Cockroach[(CockroachDB vector table)]
```

## Forecasting Flow

```mermaid
flowchart TD
    AEHistory[A&E monthly activity table] --> Trend[Simple linear trend]
    Trend --> Forecast[3-month pressure forecast]
    Forecast --> Context[Forecast context]
    Context --> Bedrock[AWS Bedrock answer]
```

The forecast is a prototype decision-support signal. It is not an official NHS prediction.

## Deployment

The app is deployed on Vercel:

```text
https://nhs-healthcare-capacity-ai.vercel.app
```

Vercel stores deployment secrets as private environment variables:

- `DATABASE_URL`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`
- `EMBEDDING_PROVIDER`
- `EMBEDDING_MODEL`
- `BEDROCK_TEXT_MODEL`

The local `.env` file is ignored by Git and must never be committed.
