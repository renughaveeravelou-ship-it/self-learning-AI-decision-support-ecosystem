from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from dashboard.core import ROOT_DIR


def render() -> None:
    st.title("Feedback Analytics")

    feedback_path = Path(ROOT_DIR) / "feedback_log.csv"
    if not feedback_path.exists() or feedback_path.stat().st_size == 0:
        st.info("No feedback has been recorded yet.")
        return

    df = pd.read_csv(feedback_path)
    df = df.rename(columns={"rec1": "recommendation", "outcome1": "outcome"})
    if "outcome" in df.columns:
        df["outcome"] = df["outcome"].replace({"Agree": "success", "Disagree": "failed"})

    st.dataframe(df, use_container_width=True)

    if "outcome" not in df.columns:
        st.warning("Feedback log does not contain an outcome column.")
        return

    try:
        import plotly.express as px
        from analytics.decision_scoring import calculate_score
    except Exception as exc:
        st.warning(f"Analytics visualizations are unavailable: {exc}")
        return

    df["score"] = df["outcome"].apply(calculate_score)
    col1, col2 = st.columns(2)
    col1.metric("Average Outcome Score", f"{df['score'].mean():.2f}")
    col2.metric("Agreement Rate", f"{(df['outcome'] == 'success').mean() * 100:.1f}%")
    st.plotly_chart(px.pie(df, names="outcome"), use_container_width=True)

