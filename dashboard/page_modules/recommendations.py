from __future__ import annotations

import streamlit as st

from dashboard.core import build_recommendations, init_session_state, save_feedback_entry, train_all_models


def render() -> None:
    init_session_state()
    st.title("Recommendations")
    st.caption("Live recommendations with a feedback loop.")

    try:
        from agents.agent_orchestrator import run_agents
        from decision_engine.recommendation_engine import generate_recommendations
    except Exception as exc:
        st.error(f"Recommendation engine unavailable: {exc}")
        return

    if st.button("Refresh Recommendations"):
        st.session_state.recommendations = build_recommendations()
        st.session_state.rag_service.build_index(st.session_state.recommendations)
        st.session_state.rag_built = True

    recs = generate_recommendations(run_agents())
    if st.button("Trigger Model Retraining"):
        with st.spinner("Retraining all models..."):
            train_all_models()
        st.success("Retraining completed.")

    for idx, rec in enumerate(recs):
        st.markdown(f"**Recommendation #{idx + 1}**  \n{rec}")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Agree", key=f"agree_{idx}"):
                save_feedback_entry(rec, "Agree")
        with c2:
            if st.button("Disagree", key=f"disagree_{idx}"):
                save_feedback_entry(rec, "Disagree")

