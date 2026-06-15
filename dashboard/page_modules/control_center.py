from __future__ import annotations

import streamlit as st

from dashboard.core import build_recommendations, init_session_state, load_metrics, train_all_models


def render() -> None:
    init_session_state()
    st.title("Control Center")
    st.caption("Model retraining and current system metrics.")

    if st.button("Start Retraining", type="primary"):
        with st.spinner("Retraining models..."):
            train_all_models()
            st.session_state.recommendations = build_recommendations()
            st.session_state.rag_service.build_index(st.session_state.recommendations)
            st.session_state.rag_built = True
        st.success("Retraining complete.")

    st.subheader("Metrics")
    st.json(load_metrics())

