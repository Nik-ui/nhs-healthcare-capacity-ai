from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

BEDS_FILE = RAW_DIR / "Beds-Open-Overnight-Web_File-Q3-2025-26_duplicate.xlsx"
AE_FILE = RAW_DIR / "Monthly-AE-Time-Series-January-2026-C86cfU_duplicate.xls"


def clean_column_name(value: object) -> str:
    text = str(value).strip().lower()
    text = text.replace("&", "and")
    text = text.replace(">", "over")
    text = text.replace("%", "pct")
    text = text.replace("(", "")
    text = text.replace(")", "")
    text = text.replace("/", " ")
    text = text.replace("-", " ")
    text = text.replace(".", "")
    text = text.replace(",", "")
    text = text.replace("ie ", "")
    text = "_".join(text.split())
    return text


def fiscal_period_to_date(year: str, month_name: str) -> pd.Timestamp:
    start_year = int(str(year).split("-")[0])
    month = pd.to_datetime(month_name, format="%B").month
    calendar_year = start_year + 1 if month <= 3 else start_year
    return pd.Timestamp(year=calendar_year, month=month, day=1)


def risk_band(score: float) -> str:
    if score >= 85:
        return "critical"
    if score >= 70:
        return "high"
    if score >= 55:
        return "elevated"
    return "normal"


def scaled(value: float, low: float, high: float) -> float:
    if pd.isna(value):
        return 0.0
    if high == low:
        return 0.0
    return max(0.0, min(1.0, (float(value) - low) / (high - low)))


def load_beds() -> pd.DataFrame:
    beds = pd.read_excel(BEDS_FILE, sheet_name="Region by Sector", header=14)
    beds = beds.dropna(how="all").copy()
    beds = beds.drop(columns=[c for c in beds.columns if str(c).startswith("Unnamed")])

    beds.loc[beds["AT Name"].eq("England") & beds["Region Code"].isna(), "Region Code"] = "ENG"
    beds["AT Name"] = beds["AT Name"].astype(str).str.strip().str.upper()

    beds = beds.rename(
        columns={
            "Total ": "beds_available_total",
            "General & Acute": "ga_available",
            "Total .1": "beds_occupied_total",
            "General & Acute.1": "ga_occupied",
            "Total .2": "beds_occupancy_rate",
            "General & Acute.2": "ga_occupancy_rate",
        }
    )

    beds["period_date"] = [
        fiscal_period_to_date(year, month)
        for year, month in zip(beds["Year"], beds["Period End"], strict=False)
    ]

    keep_columns = [
        "period_date",
        "Year",
        "Period End",
        "Region Code",
        "AT Name",
        "beds_available_total",
        "ga_available",
        "beds_occupied_total",
        "ga_occupied",
        "beds_occupancy_rate",
        "ga_occupancy_rate",
    ]
    beds = beds[keep_columns].rename(
        columns={
            "Year": "reporting_year",
            "Period End": "period_end",
            "Region Code": "region_code",
            "AT Name": "region_name",
        }
    )

    numeric_columns = [
        "beds_available_total",
        "ga_available",
        "beds_occupied_total",
        "ga_occupied",
        "beds_occupancy_rate",
        "ga_occupancy_rate",
    ]
    beds[numeric_columns] = beds[numeric_columns].apply(pd.to_numeric, errors="coerce")
    return beds.sort_values(["period_date", "region_name"]).reset_index(drop=True)


def load_ae_activity() -> pd.DataFrame:
    ae = pd.read_excel(AE_FILE, sheet_name="Activity", header=13)
    ae = ae.drop(columns=[c for c in ae.columns if str(c).startswith("Unnamed") or not isinstance(c, str)])
    ae = ae.dropna(subset=["Period"]).copy()

    ae.columns = [clean_column_name(c) for c in ae.columns]
    ae = ae.rename(
        columns={
            "period": "period_date",
            "type_1_departments_major_aande": "ae_type_1_attendances",
            "type_2_departments_single_specialty": "ae_type_2_attendances",
            "type_3_departments_other_aande_minor_injury_unit": "ae_type_3_attendances",
            "total_attendances": "ae_total_attendances",
            "emergency_admissions_via_type_1_aande": "emergency_admissions_via_type_1_ae",
            "emergency_admissions_via_type_2_aande": "emergency_admissions_via_type_2_ae",
            "emergency_admissions_via_type_3_and_4_aande": "emergency_admissions_via_type_3_4_ae",
            "total_emergency_admissions_via_aande": "emergency_admissions_via_ae",
            "other_emergency_admissions_not_via_aande": "other_emergency_admissions",
            "number_of_patients_spending_over4_hours_from_decision_to_admit_to_admission": "dta_waits_over_4h",
            "number_of_patients_spending_over12_hours_from_decision_to_admit_to_admission": "dta_waits_over_12h",
            "operational_standard_performance": "operational_standard",
        }
    )

    ae["period_date"] = pd.to_datetime(ae["period_date"]).dt.to_period("M").dt.to_timestamp()
    for column in ae.columns:
        if column != "period_date":
            ae[column] = pd.to_numeric(ae[column], errors="coerce")

    return ae.sort_values("period_date").reset_index(drop=True)


def create_national_pressure(beds: pd.DataFrame, ae: pd.DataFrame) -> pd.DataFrame:
    england_beds = beds[beds["region_name"].eq("ENGLAND")].copy()
    merged = england_beds.merge(ae, on="period_date", how="inner")

    merged["admission_rate_via_ae"] = (
        merged["emergency_admissions_via_ae"] / merged["ae_total_attendances"]
    )
    merged["dta_12h_wait_rate"] = merged["dta_waits_over_12h"] / merged["emergency_admissions_via_ae"]

    occupancy_component = merged["ga_occupancy_rate"].apply(lambda x: scaled(x, 0.80, 0.95)) * 55
    admission_component = merged["admission_rate_via_ae"].apply(lambda x: scaled(x, 0.15, 0.25)) * 25
    wait_component = merged["dta_12h_wait_rate"].apply(lambda x: scaled(x, 0.00, 0.15)) * 20

    merged["capacity_pressure_score"] = (
        occupancy_component + admission_component + wait_component
    ).round(1)
    merged["risk_band"] = merged["capacity_pressure_score"].apply(risk_band)

    return merged


def write_outputs() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    beds = load_beds()
    ae = load_ae_activity()
    pressure = create_national_pressure(beds, ae)

    beds.to_csv(PROCESSED_DIR / "beds_region_sector_clean.csv", index=False)
    ae.to_csv(PROCESSED_DIR / "ae_activity_clean.csv", index=False)
    pressure.to_csv(PROCESSED_DIR / "national_capacity_pressure.csv", index=False)

    beds.to_json(PROCESSED_DIR / "beds_region_sector_clean.json", orient="records", date_format="iso")
    ae.to_json(PROCESSED_DIR / "ae_activity_clean.json", orient="records", date_format="iso")
    pressure.to_json(PROCESSED_DIR / "national_capacity_pressure.json", orient="records", date_format="iso")

    summary = {
        "beds_rows": int(len(beds)),
        "ae_rows": int(len(ae)),
        "pressure_rows": int(len(pressure)),
        "beds_period_min": beds["period_date"].min().date().isoformat(),
        "beds_period_max": beds["period_date"].max().date().isoformat(),
        "ae_period_min": ae["period_date"].min().date().isoformat(),
        "ae_period_max": ae["period_date"].max().date().isoformat(),
        "latest_common_period": (
            pressure["period_date"].max().date().isoformat() if not pressure.empty else None
        ),
        "risk_score_note": (
            "Prototype score using weighted occupancy, admissions via A&E, and 12-hour "
            "decision-to-admit wait rate. Thresholds are product assumptions and must "
            "not be interpreted as official NHS risk classifications."
        ),
    }
    (PROCESSED_DIR / "data_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    write_outputs()
