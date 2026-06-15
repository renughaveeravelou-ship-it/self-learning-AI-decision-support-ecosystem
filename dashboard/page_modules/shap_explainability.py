from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from dashboard.core import ROOT_DIR


def render() -> None:
    st.title("SHAP Explainability")

    try:
        from explainability.shap_analysis import explain_model
    except Exception as exc:
        st.error(f"Explainability module unavailable: {exc}")
        return

    sales_data_path = Path(ROOT_DIR) / "Sales Data.csv"
    sales_model_path = Path(ROOT_DIR) / "saved_models" / "sales_model.joblib"
    if not sales_data_path.exists() or not sales_model_path.exists():
        st.warning("Sales data or model artifact not found.")
        return

    df = pd.read_csv(sales_data_path)
    X = df.drop(columns=["profit"], errors="ignore").head(20)
    explain_model(str(sales_model_path), X)

