# Deployment Guide

This project can be deployed as a small FastAPI web service.

## Recommended hackathon path

Use Render for the public demo URL.

Why:

- it has a free web service option
- it can deploy directly from GitHub
- it supports Python/FastAPI
- it lets us keep secrets as private environment variables

Important: the free service may sleep after inactivity. If the page is slow on first load, refresh after it wakes up.

## Environment variables

Add these in the Render dashboard. Do not put real values in GitHub.

```text
DATABASE_URL=your CockroachDB connection string
AWS_ACCESS_KEY_ID=your AWS access key id
AWS_SECRET_ACCESS_KEY=your AWS secret access key
AWS_REGION=us-east-1
EMBEDDING_PROVIDER=bedrock
EMBEDDING_MODEL=amazon.titan-embed-text-v2:0
BEDROCK_TEXT_MODEL=anthropic.claude-sonnet-4-20250514-v1:0
```

## Start command

Render uses this command:

```text
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Meaning:

- `uvicorn` runs the FastAPI app
- `app.main:app` points to the `app` object in `app/main.py`
- `0.0.0.0` allows Render to expose it publicly
- `$PORT` uses the port Render assigns automatically

## Test after deployment

Open:

```text
https://your-render-url.onrender.com
```

Then test:

```text
https://your-render-url.onrender.com/health
```

Expected result:

```json
{"status":"ok","service":"NHS Capacity Memory Agent API"}
```
