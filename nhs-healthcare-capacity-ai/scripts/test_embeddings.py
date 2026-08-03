import sys
from pathlib import Path


project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from agent.embeddings import generate_embedding


embedding = generate_embedding("What is NHS capacity pressure?")

print("Generated embedding successfully.")
print(f"Embedding dimensions: {len(embedding)}")
print(f"First 5 values: {embedding[:5]}")
