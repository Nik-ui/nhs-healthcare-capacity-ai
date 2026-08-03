import sys
from pathlib import Path


project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from agent.bedrock_client import generate_text


prompt = "Explain NHS bed occupancy in one beginner-friendly sentence."

answer = generate_text(prompt)

print("Bedrock answer:")
print(answer)