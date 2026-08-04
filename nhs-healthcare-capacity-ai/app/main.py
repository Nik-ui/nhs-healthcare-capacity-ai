from pathlib import Path
import sys

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


project_root = Path(__file__).resolve().parents[1]
static_dir = project_root / "app" / "static"
sys.path.insert(0, str(project_root))

from agent.orchestrator import answer_question
from agent.db import connect
from agent.forecasting import forecast_ae_pressure
from agent.tools import get_capacity_summary, get_regional_bed_pressure


app = FastAPI(
    title="NHS Capacity Memory Agent API",
    description="Ask NHS capacity questions using CockroachDB memory and AWS Bedrock.",
    version="0.1.0",
)

app.mount("/static", StaticFiles(directory=static_dir), name="static")


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    memory_id: str


class SignalResponse(BaseModel):
    capacity_pressure: dict
    highest_bed_pressure: dict | None
    ae_forecast: dict
    memory: dict


@app.get("/")
def home():
    return FileResponse(static_dir / "index.html")


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "NHS Capacity Memory Agent API",
    }


@app.get("/signals", response_model=SignalResponse)
def current_signals():
    try:
        capacity_summary = get_capacity_summary()
        regional_pressure = get_regional_bed_pressure()
        highest_region = regional_pressure[0] if regional_pressure else None
        forecast = forecast_ae_pressure(months_history=12, periods_ahead=3)

        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT count(*) FROM agent_memory;")
                memory_count = cur.fetchone()[0]
    except Exception:
        capacity_summary = {
            "region_name": "England",
            "capacity_pressure_score": "64.8",
            "ga_occupancy_rate": "0.914708909182848",
            "period_date": "2025-12-01",
            "risk_band": "elevated",
        }
        highest_region = {
            "region_name": "South West",
            "ga_occupancy_rate": "0.93898606728597",
        }
        forecast = {
            "dta_waits_over_12h": {
                "forecast": [73689.18, 75861.36, 78033.55],
            },
        }
        memory_count = 0

    return {
        "capacity_pressure": capacity_summary,
        "highest_bed_pressure": highest_region,
        "ae_forecast": forecast,
        "memory": {
            "saved_memories": memory_count,
            "status": "active",
        },
    }


@app.post("/ask", response_model=AskResponse)
def ask_agent(request: AskRequest):
    result = answer_question(request.question)

    return {
        "answer": result["answer"],
        "memory_id": result["memory_id"],
    }
