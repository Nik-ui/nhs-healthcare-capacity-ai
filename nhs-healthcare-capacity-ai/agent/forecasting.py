from decimal import Decimal

from agent.tools import get_ae_time_trend


def to_float(value):
    if value is None:
        return None

    if isinstance(value, Decimal):
        return float(value)

    return float(value)


def calculate_linear_forecast(values, periods_ahead=3):
    clean_values = [to_float(value) for value in values if value is not None]

    if len(clean_values) < 2:
        return None

    first_value = clean_values[0]
    last_value = clean_values[-1]
    monthly_change = (last_value - first_value) / (len(clean_values) - 1)

    forecast = []

    for step in range(1, periods_ahead + 1):
        forecast.append(last_value + (monthly_change * step))

    return {
        "first_value": first_value,
        "last_value": last_value,
        "monthly_change": monthly_change,
        "forecast": forecast,
    }


def forecast_ae_pressure(months_history=12, periods_ahead=3):
    history = get_ae_time_trend(months=months_history)

    attendances = [row["ae_total_attendances"] for row in history]
    admissions = [row["emergency_admissions_via_ae"] for row in history]
    waits_12h = [row["dta_waits_over_12h"] for row in history]

    return {
        "tool": "forecast_ae_pressure",
        "method": "simple_linear_trend",
        "history_months_used": len(history),
        "periods_ahead": periods_ahead,
        "ae_total_attendances": calculate_linear_forecast(attendances, periods_ahead),
        "emergency_admissions_via_ae": calculate_linear_forecast(admissions, periods_ahead),
        "dta_waits_over_12h": calculate_linear_forecast(waits_12h, periods_ahead),
    }