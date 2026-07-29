# Hackathon Strategy

This project is being shaped for the CockroachDB x AWS Hackathon: Build with Agentic Memory.

Official hackathon page:

https://cockroachdb-ai.devpost.com/

## What The Hackathon Requires

The submission must be an agentic application that:

- uses CockroachDB as a persistent memory layer
- is deployed on AWS
- uses at least two CockroachDB tools
- uses at least one AWS service
- has a public open-source repository
- has a functional demo app URL
- includes a public demo video under 3 minutes

## Required CockroachDB Fit

The project should use CockroachDB for real agent memory, not just as a storage checkbox.

Recommended CockroachDB tools for this project:

| Tool | How We Use It |
|---|---|
| CockroachDB Cloud | Main database for NHS capacity snapshots, agent memory, and recommendations |
| Distributed Vector Indexing | Store embeddings for semantic retrieval of past capacity patterns and agent notes |
| Managed MCP Server | Let an AI coding or agent workflow inspect/query CockroachDB safely during development |
| ccloud CLI | Optional: show infrastructure setup and database management from the terminal |

Minimum recommended pair:

- CockroachDB Cloud
- Distributed Vector Indexing

Stretch pair:

- Managed MCP Server
- ccloud CLI

## Required AWS Fit

Recommended AWS service:

| AWS Service | How We Use It |
|---|---|
| AWS Lambda | Run the agent API or scheduled data refresh as a serverless function |
| Amazon Bedrock | Optional model layer for summaries, recommendations, or agent reasoning |
| Amazon S3 | Optional storage for source files, exports, screenshots, or demo artifacts |

Minimum recommended AWS path:

- AWS Lambda for agent execution

Stronger path:

- AWS Lambda + Amazon Bedrock

## Product Pivot

Original idea:

NHS Capacity Intelligence Dashboard

Hackathon-ready idea:

NHS Capacity Memory Agent

The dashboard still matters, but the core product becomes an agent that can remember previous capacity pressure patterns and use that memory to answer current operational questions.

## Winning MVP

The first version should support this flow:

1. User asks: "What is the current NHS capacity pressure?"
2. Agent reads the latest processed NHS capacity metrics.
3. Agent retrieves similar historical periods or stored notes from CockroachDB memory.
4. Agent explains the current pressure level.
5. Agent suggests what operational teams should monitor next.
6. Agent stores the question, answer, retrieved memories, and recommendation back into CockroachDB.

## Core Demo Moments

The demo video should show:

- the NHS metrics dashboard
- an agent question and answer
- a visible memory log written to CockroachDB
- semantic retrieval of similar pressure context
- AWS service involvement
- a clear explanation of why CockroachDB is the durable memory layer

## Proposed Architecture

```text
NHS raw data
  -> Python data preparation
  -> CockroachDB tables
      -> capacity_snapshots
      -> agent_memory
      -> memory_embeddings
      -> recommendations
  -> Agent API on AWS Lambda
  -> React dashboard and agent chat UI
```

## Suggested Database Tables

| Table | Purpose |
|---|---|
| `capacity_snapshots` | Stores structured NHS metrics by period and region |
| `agent_memory` | Stores user questions, answers, reasoning summaries, and timestamps |
| `memory_embeddings` | Stores vector embeddings for semantic memory retrieval |
| `recommendations` | Stores agent-generated monitoring recommendations |

## Judging Strategy

| Judging Area | How We Compete |
|---|---|
| Agentic Memory Design | Make memory visible and essential to the user experience |
| Technical Implementation | Use CockroachDB for structured data and vector search, plus AWS deployment |
| Real-World Impact | Focus on healthcare operations pressure, a meaningful public-sector workflow |
| Production Readiness | Add clear setup docs, schema, logging, limitations, and safe disclaimers |
| Creativity | Position the product as an agent that remembers pressure patterns, not a normal chatbot |

## Immediate Build Order

1. Rename/reframe product docs around `NHS Capacity Memory Agent`.
2. Create CockroachDB schema SQL.
3. Write a loader script to push processed NHS data into CockroachDB.
4. Build a simple agent API locally.
5. Store every interaction as agent memory.
6. Add vector search for semantic memory retrieval.
7. Build the React demo UI.
8. Deploy with AWS.
9. Record a short demo video.
