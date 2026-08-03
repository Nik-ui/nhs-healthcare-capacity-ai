import sys
from pathlib import Path


project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from agent.forecasting import forecast_ae_pressure


forecast = forecast_ae_pressure(months_history=12, periods_ahead=3)

print("A&E pressure forecast:")
print(forecast)