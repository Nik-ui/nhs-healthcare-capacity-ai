# Devpost Submission

## Project Title

NHS Capacity Memory Agent

## Short Description

A health operations assistant that uses CockroachDB Cloud, CockroachDB vector search, and AWS Bedrock to answer NHS capacity questions, recall previous discussions, and forecast short-term A&E pressure.

## Inspiration

Emergency care pressure is difficult to understand quickly because bed occupancy, A&E attendances, emergency admissions, and long waits are often reported across separate files and periods. Operational users need more than a dashboard: they need a system they can ask questions, return to later, and use to build an ongoing memory of capacity pressure.

NHS Capacity Memory Agent explores what this could look like: a data-grounded assistant that turns public NHS England capacity data into practical answers and remembers previous interactions.

## What It Does

The app lets a user ask natural-language questions such as:

- Which region has the highest bed occupancy?
- What is the likely A&E pressure trend over the next 3 months?
- What did I ask earlier about capacity pressure?

The agent retrieves NHS context from CockroachDB, runs a short-term A&E pressure forecast, searches previous memories using vector search, asks AWS Bedrock to generate an answer, then saves the new question and answer back into CockroachDB memory.

## How We Built It

The system is built with:

- FastAPI for the API and deployed web application
- CockroachDB Cloud for structured NHS data and persistent memory
- CockroachDB vector search for semantic memory retrieval
- AWS Bedrock for answer generation
- Bedrock Titan embeddings for memory vectors
- Python data scripts for cleaning and loading NHS England data
- Vercel for the polished public demo deployment
- AWS Lambda Function URL for AWS-hosted API deployment evidence

The database stores national capacity snapshots, regional bed pressure, A&E activity history, agent memory, vector embeddings, and recommendation-ready records.

## CockroachDB Usage

CockroachDB is central to the project. It is not used only as a storage layer.

CockroachDB stores:

- NHS capacity snapshots
- regional bed occupancy data
- A&E monthly activity data
- previous user questions
- previous agent answers
- vector embeddings for semantic memory retrieval
- recommendation records

The agent queries CockroachDB every time it answers a question. CockroachDB vector search retrieves previous memories that are similar to the new user question.

## AWS Usage

AWS Bedrock is used for:

- answer generation from retrieved project context
- Bedrock Titan embeddings for memory vectors

This keeps the model separate from the database memory layer, while allowing the app to combine structured operational data with language reasoning.

## Data Used

The project uses public NHS England datasets:

- Bed Availability and Occupancy, Q3 2025-26
- Monthly A&E Attendances and Emergency Admissions, January 2026

The current demo loads:

- 1 national capacity pressure row
- 8 regional bed pressure rows
- 186 A&E activity rows

## Key Features

- deployed public web app
- natural-language capacity questions
- CockroachDB-backed memory
- CockroachDB vector similarity search
- A&E pressure forecasting
- AWS Bedrock answer generation
- operationally focused UI
- memory ID evidence for saved interactions

## Challenges

The main challenge was turning notebook-style exploratory analysis into a working product. The work involved cleaning NHS data, designing a CockroachDB schema, handling vector dimensions correctly, connecting AWS Bedrock, and deploying a FastAPI app with private environment variables.

Another challenge was making the agent answer naturally while still grounding answers in retrieved database context. The final version keeps the technical architecture visible in the product and documentation, but keeps the user-facing answer clean.

## What We Learned

This project helped clarify how an assistant can be built around a reliable data store rather than only prompt logic. CockroachDB provides the system memory, AWS Bedrock provides language reasoning, and the app layer turns both into a user-facing product.

We also learned the importance of separating:

- data retrieval
- memory retrieval
- forecast generation
- answer generation
- memory persistence

That separation makes the project easier to explain, test, and extend.

## What's Next

Next improvements:

- add richer forecasting methods
- add charts for regional and A&E trends
- expand the NHS dataset coverage
- add a recommendation engine for operational actions
- add LangGraph orchestration for explicit agent state
- add authentication and role-based workflows for real users

## Demo Link

https://nhs-healthcare-capacity-ai.vercel.app

AWS Lambda Function URL:

https://yul47sn53pnghl73lmiacl444u0jqoxt.lambda-url.us-east-1.on.aws

## Repository

https://github.com/Nik-ui/nhs-healthcare-capacity-ai
