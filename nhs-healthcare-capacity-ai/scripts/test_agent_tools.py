import sys
from pathlib import Path


project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from agent.tools import (
    get_ae_activity_history,
    get_capacity_summary,
    get_regional_bed_pressure,
)


print("Capacity summary:")
print(get_capacity_summary())

print()
print("Regional bed pressure:")
for row in get_regional_bed_pressure():
    print(row)

print()
print("Recent A&E activity:")
for row in get_ae_activity_history(limit=5):
    print(row)