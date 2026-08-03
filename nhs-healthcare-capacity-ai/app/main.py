from pathlib import Path
import sys

from fastapi import FastAPI
from pydantic import BaseModel


project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from agent.orchestrator import answer_question


app = FastAPI(
    title="NHS Capacity Memory Agent API",
    description="Ask NHS capacity questions using CockroachDB memory and AWS Bedrock.",
    version="0.1.0",
)


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    memory_id: str


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "service": "NHS Capacity Memory Agent API",
    }


@app.post("/ask", response_model=AskResponse)
def ask_agent(request: AskRequest):
    result = answer_question(request.question)

    return {
        "answer": result["answer"],
        "memory_id": result["memory_id"],
    }
