import sys
from pathlib import Path


project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from agent.orchestrator import answer_question


print("NHS Capacity Memory Agent")
print("Ask about capacity pressure, A&E trends, regional bed pressure, or memory.")
print()

user_question = input("Your question: ").strip()

if not user_question:
    raise ValueError("Question cannot be empty.")

result = answer_question(user_question)

print()
print("Agent answer:")
print(result["answer"])

print()
print("Saved to CockroachDB memory.")
print(f"Memory ID: {result['memory_id']}")