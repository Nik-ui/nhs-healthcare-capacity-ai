import sys
from pathlib import Path


project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from agent.memory import get_recent_memories, save_memory


memory_id = save_memory(
    user_question="Test memory: what is this project storing?",
    agent_answer="The project stores NHS capacity data and agent memory in CockroachDB.",
    memory_summary="Test memory confirming CockroachDB stores NHS data and agent memory.",
    retrieved_context="Manual test from scripts/test_agent_memory.py",
)

print("Saved memory:")
print(memory_id)

print()
print("Recent memories:")
for memory in get_recent_memories(limit=5):
    print(memory)