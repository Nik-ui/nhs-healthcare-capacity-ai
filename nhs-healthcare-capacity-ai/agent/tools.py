from agent.db import connect


def get_capacity_summary():
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    period_date,
                    region_name,
                    ga_occupancy_rate,
                    ae_total_attendances,
                    emergency_admissions_via_ae,
                    dta_waits_over_12h,
                    capacity_pressure_score,
                    risk_band
                FROM capacity_snapshots
                ORDER BY period_date DESC
                LIMIT 1;
            """)

            row = cur.fetchone()

    if not row:
        return "No capacity summary data found."

    (
        period_date,
        region_name,
        ga_occupancy_rate,
        ae_total_attendances,
        emergency_admissions_via_ae,
        dta_waits_over_12h,
        capacity_pressure_score,
        risk_band,
    ) = row

    return {
        "tool": "get_capacity_summary",
        "period_date": str(period_date),
        "region_name": region_name,
        "ga_occupancy_rate": str(ga_occupancy_rate),
        "ae_total_attendances": str(ae_total_attendances),
        "emergency_admissions_via_ae": str(emergency_admissions_via_ae),
        "dta_waits_over_12h": str(dta_waits_over_12h),
        "capacity_pressure_score": str(capacity_pressure_score),
        "risk_band": risk_band,
    }


def get_regional_bed_pressure():
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    period_date,
                    region_code,
                    region_name,
                    ga_available,
                    ga_occupied,
                    ga_occupancy_rate
                FROM beds_region_sector
                ORDER BY ga_occupancy_rate DESC;
            """)

            rows = cur.fetchall()

    return [
        {
            "period_date": str(row[0]),
            "region_code": row[1],
            "region_name": row[2],
            "ga_available": str(row[3]),
            "ga_occupied": str(row[4]),
            "ga_occupancy_rate": str(row[5]),
        }
        for row in rows
    ]


def get_ae_activity_history(limit=12):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    period_date,
                    ae_total_attendances,
                    emergency_admissions_via_ae,
                    dta_waits_over_4h,
                    dta_waits_over_12h
                FROM ae_activity
                ORDER BY period_date DESC
                LIMIT %(limit)s;
                """,
                {"limit": limit},
            )

            rows = cur.fetchall()

    return [
        {
            "period_date": str(row[0]),
            "ae_total_attendances": str(row[1]),
            "emergency_admissions_via_ae": str(row[2]),
            "dta_waits_over_4h": str(row[3]),
            "dta_waits_over_12h": str(row[4]),
        }
        for row in rows
    ]


def get_ae_time_trend(months=6):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    period_date,
                    ae_total_attendances,
                    emergency_admissions_via_ae,
                    dta_waits_over_4h,
                    dta_waits_over_12h
                FROM ae_activity
                ORDER BY period_date DESC
                LIMIT %(months)s;
                """,
                {"months": months},
            )

            rows = cur.fetchall()

    rows.reverse()

    return [
        {
            "period_date": str(row[0]),
            "ae_total_attendances": str(row[1]),
            "emergency_admissions_via_ae": str(row[2]),
            "dta_waits_over_4h": str(row[3]),
            "dta_waits_over_12h": str(row[4]),
        }
        for row in rows
    ]