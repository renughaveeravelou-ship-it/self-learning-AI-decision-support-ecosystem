from __future__ import annotations

import os

import streamlit as st

from dashboard.core import ROOT_DIR, load_csv


def render() -> None:
    st.title("Overview Dashboard")
    st.caption("Cross-dataset operational summary.")

    try:
        import joblib
        import plotly.express as px
    except Exception as exc:
        st.error(f"Visualization dependencies are unavailable: {exc}")
        return

    df_customer = load_csv("Customer data.csv")
    df_sales = load_csv("Sales Data.csv")
    df_market = load_csv("market Data.csv")
    df_social = load_csv("Social Medis Data.csv")
    df_iot = load_csv("IoT data.csv")

    metrics = [
        ("Net Sales Profit", df_sales["profit"].sum() if df_sales is not None and "profit" in df_sales else None),
        ("Avg Customer Rating", df_market["Rating"].mean() if df_market is not None and "Rating" in df_market else None),
        ("Avg Engagement", df_social["Engagement_Rate"].mean() if df_social is not None and "Engagement_Rate" in df_social else None),
        ("Fleet Size", "261,461"),
        ("IoT Alerts", int(df_iot["Failure_Within_7_Days"].sum()) if df_iot is not None and "Failure_Within_7_Days" in df_iot else None),
    ]

    for column, (label, value) in zip(st.columns(5), metrics):
        with column:
            st.metric(label, "N/A" if value is None else value)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Customer Segments")
        if df_customer is None:
            st.info("Customer dataset not found.")
        else:
            model_path = ROOT_DIR / "saved_models" / "customer_kmeans.joblib"
            data = df_customer.copy()
            if model_path.exists():
                model = joblib.load(model_path)
                data["Cluster"] = model.predict(data[["Annual_Income_(k$)", "Spending_Score"]])
            else:
                data["Cluster"] = 0
            fig = px.scatter(data, x="Annual_Income_(k$)", y="Spending_Score", color=data["Cluster"].astype(str))
            st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.subheader("Profit vs Cost")
        if df_sales is None:
            st.info("Sales dataset not found.")
        else:
            grouped = df_sales.groupby("category")[["profit", "cost"]].sum().reset_index()
            st.plotly_chart(px.bar(grouped, x="category", y=["profit", "cost"], barmode="group"), use_container_width=True)

