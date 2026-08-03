# Vercel Deployment Guide

Vercel is a good public demo option because it can run FastAPI apps without keeping a sleeping server alive.

## Why Vercel

- free Hobby plan for personal projects
- deploys from GitHub
- supports FastAPI through the Python runtime
- does not expose `.env` secrets in GitHub
- gives a public URL for judges

Vercel runs the FastAPI app as a function. This means there can still be a short cold start, but it is not the same as a free server sleeping for 15 minutes.

## Files added for Vercel

```text
app.py
.python-version
```

`app.py` points Vercel to the existing FastAPI application:

```python
from app.main import app
```

`.python-version` tells Vercel which Python version to use.

## Environment variables

Add these in Vercel project settings:

```text
DATABASE_URL
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION
EMBEDDING_PROVIDER
EMBEDDING_MODEL
BEDROCK_TEXT_MODEL
```

Use the same values from your private local `.env` file. Do not paste the values into GitHub.

## Test URLs

After deployment, test:

```text
https://your-vercel-url.vercel.app
https://your-vercel-url.vercel.app/health
https://your-vercel-url.vercel.app/docs
```
