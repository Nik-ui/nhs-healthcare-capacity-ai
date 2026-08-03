from agent.bedrock_client import generate_text
from agent.memory import get_recent_memories, save_memory
from agent.tools import (
    get_ae_time_trend,
    get_capacity_summary,
    get_regional_bed_pressure,
)


def build_agent_context():
    capacity_summary = get_capacity_summary()
    regional_bed_pressure = get_regional_bed_pressure()
    ae_time_trend = get_ae_time_trend(months=6)
    recent_memories = get_recent_memories(limit=5)

    return {
        "capacity_summary": capacity_summary,
        "regional_bed_pressure": regional_bed_pressure,
        "ae_time_trend": ae_time_trend,
        "recent_memories": recent_memories,
    }


def answer_question(user_question):
    context = build_agent_context()

    prompt = f"""
You are the NHS Capacity Memory Agent.

You help healthcare operations teams understand NHS capacity pressure using:
1. CockroachDB NHS capacity data
2. CockroachDB stored agent memory
3. AWS Bedrock reasoning

User question:
{user_question}

CockroachDB context:
{context}

Instructions:
- Answer only using the provided CockroachDB context.
- If the context does not contain enough data, say what is missing.
- Be clear, practical, and concise.
- If useful, mention the specific period/date used.
- If the question asks for a recommendation, give operationally sensible next steps.
- Do not claim this is official NHS risk classification.
"""

    agent_answer = generate_text(prompt)

    memory_summary = (
        f"User asked: {user_question}. Agent answered using CockroachDB NHS "
        f"capacity data, recent A&E trend data, regional bed pressure data, "
        f"and recent stored memories."
    )

    memory_id = save_memory(
        user_question=user_question,
        agent_answer=agent_answer,
        memory_summary=memory_summary,
        retrieved_context=str(context),
    )

    return {
        "answer": agent_answer,
        "memory_id": str(memory_id),
        "context": context,
    }