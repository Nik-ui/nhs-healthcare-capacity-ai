# Demo Recording Guide

Target length: 90 seconds to 2 minutes.

## Story To Record

1. Show homepage.
2. Ask: Which region has the highest bed occupancy?
3. Ask: What is the likely A&E pressure trend over the next 3 months?
4. Ask: What did I ask earlier about capacity pressure?
5. Show that it remembers previous questions.
6. Briefly mention CockroachDB, Bedrock, vector memory, and AWS Lambda.

## Voiceover Script

Emergency care pressure is hard to understand quickly because bed occupancy, A&E demand, admissions, and long waits are usually spread across separate datasets. I built NHS Capacity Memory Agent to turn those signals into a question-answering assistant.

On the homepage, users can ask plain-English capacity questions. The app is deployed online, and the backend is also available through an AWS Lambda Function URL.

First, I ask: Which region has the highest bed occupancy? The agent retrieves regional bed pressure from CockroachDB and answers using the stored NHS data.

Next, I ask: What is the likely A&E pressure trend over the next 3 months? The agent uses recent A&E activity and a simple forecasting tool to produce a short-term trend signal. It also explains that this is not an official NHS prediction.

Finally, I ask: What did I ask earlier about capacity pressure? The assistant recalls previous questions because useful interactions are saved into CockroachDB memory. The project also includes vector memory, so similar questions can be retrieved semantically rather than only by exact text matching.

The architecture uses CockroachDB Cloud for NHS data, memory, and vector search; AWS Bedrock for answer generation; AWS Lambda for the API runtime; and Vercel for the frontend.

This is NHS Capacity Memory Agent: a deployed AI assistant for capacity pressure, A&E demand forecasting, and operational memory.

## Demo Links

- Frontend: https://nhs-healthcare-capacity-ai.vercel.app/
- Lambda API: https://yul47sn53pnghl73lmiacl444u0jqoxt.lambda-url.us-east-1.on.aws/
- API health check: https://yul47sn53pnghl73lmiacl444u0jqoxt.lambda-url.us-east-1.on.aws/health
- GitHub: https://github.com/Nik-ui/nhs-healthcare-capacity-ai

## Files Created

- Silent draft video: `nhs_capacity_memory_agent_demo_draft.mp4`
- Slide images: `docs/demo_assets/demo_video_slides/`

Use the silent draft as a visual guide. For the final Devpost video, record your browser while following this script so judges see the live app working.
