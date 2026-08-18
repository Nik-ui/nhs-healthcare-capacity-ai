# Deployment Guide

The project is deployed in two places:

- Vercel hosts the public web interface.
- AWS Lambda exposes the FastAPI app through a Function URL.

This gives judges a clean product link and also shows the AWS deployment required by the hackathon.

## Live URLs

Web app:

```text
https://nhs-healthcare-capacity-ai.vercel.app
```

AWS Lambda Function URL:

```text
https://yul47sn53pnghl73lmiacl444u0jqoxt.lambda-url.us-east-1.on.aws/
```

## Environment Variables

These values are configured privately in the deployment platforms. Real values must not be committed to GitHub.

```text
DATABASE_URL=your CockroachDB connection string
AWS_ACCESS_KEY_ID=your AWS access key id
AWS_SECRET_ACCESS_KEY=your AWS secret access key
AWS_REGION=us-east-1
EMBEDDING_PROVIDER=bedrock
EMBEDDING_MODEL=amazon.titan-embed-text-v2:0
BEDROCK_TEXT_MODEL=amazon.nova-pro-v1:0
```

## Local Run Command

Run the FastAPI app locally with:

```text
uvicorn app.main:app --reload
```

Meaning:

- `uvicorn` runs the FastAPI app
- `app.main:app` points to the `app` object in `app/main.py`
- `--reload` restarts the local server when code changes

## Test After Deployment

Open:

```text
https://nhs-healthcare-capacity-ai.vercel.app
```

Health checks:

```text
https://nhs-healthcare-capacity-ai.vercel.app/health
https://yul47sn53pnghl73lmiacl444u0jqoxt.lambda-url.us-east-1.on.aws/health
```

Expected result:

```json
{"status":"ok","service":"NHS Capacity Memory Agent API"}
```
