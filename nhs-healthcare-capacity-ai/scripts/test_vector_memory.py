import sys
from pathlib import Path


project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from agent.memory import get_similar_memories, save_memory_with_embedding


memory_id = save_memory_with_embedding(
    user_question="Which region has the highest bed occupancy?",
    agent_answer="South West has the highest General and Acute bed occupancy in the current regional dataset.",
    memory_summary="User asked about the region with the highest bed occupancy.",
    retrieved_context="Manual vector memory test.",
)

print("Saved vector memory:")
print(memory_id)

print()
print("Similar memories:")
for memory in get_similar_memories("What area has the worst capacity pressure?", limit=3):
    print(memory)
