# Demo Video Script

Target length: 90 seconds to 2 minutes.

## 0:00 - 0:10: Problem

"Emergency care pressure is hard to understand quickly because bed occupancy, A&E demand, admissions, and waits are usually spread across separate datasets. I built NHS Capacity Memory Agent to turn those signals into a question-answering assistant."

Show:

- homepage
- title and current signals

## 0:10 - 0:30: Product Overview

"The app uses public NHS England data, stores it in CockroachDB Cloud, uses AWS Bedrock to generate answers, and saves previous questions as memory."

Show:

- CockroachDB badge
- Bedrock badge
- Current Signals panel
- glossary and demo story

## 0:30 - 0:55: Ask A Capacity Question

Ask:

```text
Which region has the highest bed occupancy?
```

Say:

"The agent retrieves regional bed pressure from CockroachDB and answers with the highest-pressure region."

Show:

- question in the text box
- answer returned

## 0:55 - 1:20: Ask A Forecast Question

Ask:

```text
What is the likely A&E pressure trend over the next 3 months?
```

Say:

"The agent uses the A&E history table and a simple linear forecast tool. It clearly states that this is a trend signal, not an official NHS prediction."

Show:

- forecast answer with attendances, admissions, and 12-hour waits

## 1:20 - 1:40: Show Memory

Ask:

```text
What did I ask earlier about capacity pressure?
```

Say:

"Because answers are saved in CockroachDB memory, the assistant can recall previous interactions. Vector memory also supports similar-question recall."

Show:

- memory-style answer
- mention memory ID if visible in API or logs

## 1:40 - 2:00: Architecture Close

"The core architecture is FastAPI, CockroachDB Cloud, CockroachDB vector search, AWS Bedrock, and a deployed Vercel frontend. The goal is to show how a healthcare operations assistant can be grounded in real capacity data and persistent memory."

Show:

- `/docs`
- architecture or ERD markdown
- live URL

## Final Line

"This is NHS Capacity Memory Agent: a deployed AI assistant for capacity pressure, demand forecasting, and operational memory."
