from __future__ import annotations

import streamlit as st


def render() -> None:
    st.title("Drift Detector")

    try:
        from drift.drift_detector import detect_drift
    except Exception as exc:
        st.error(f"Drift detector unavailable: {exc}")
        return

    baseline = st.number_input("Baseline Accuracy", min_value=0.0, max_value=1.0, value=0.90, step=0.01)
    current = st.number_input("Current Accuracy", min_value=0.0, max_value=1.0, value=0.83, step=0.01)
    if st.button("Check Drift"):
        result = detect_drift(baseline, current)
        if result["drift_detected"]:
            st.error(f"Drift detected: {result['drift_score']:.3f}")
        else:
            st.success(f"No drift detected: {result['drift_score']:.3f}")

