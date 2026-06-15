from __future__ import annotations

import streamlit as st


def render() -> None:
    st.title("Enterprise KPI Dashboard")

    try:
        from monitoring.audit_logger import calculate_kpis
    except Exception as exc:
        st.error(f"KPI module unavailable: {exc}")
        return

    kpis = calculate_kpis()
    cols = st.columns(2)
    cols[0].metric("Customer Retention", f"{kpis['customer_retention']}%")
    cols[0].metric("Revenue Forecast", f"${kpis['revenue_forecast']:,}")
    cols[1].metric("Machine Health", f"{kpis['machine_health']}%")
    cols[1].metric("Decision Success", f"{kpis['decision_success']}%")

