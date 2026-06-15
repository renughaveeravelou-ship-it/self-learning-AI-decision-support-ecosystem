from __future__ import annotations

import streamlit as st

from dashboard.core import build_recommendations, init_session_state


def render() -> None:
    init_session_state()
    st.title("Decision Support Desk")
    st.caption("Interactive recommendation review and filtering.")

    if st.button("Generate Fresh Recommendations", type="primary"):
        st.session_state.recommendations = build_recommendations()
        st.session_state.rag_service.build_index(st.session_state.recommendations)
        st.session_state.rag_built = True

    if not st.session_state.recommendations:
        try:
            st.session_state.recommendations = build_recommendations()
            st.session_state.rag_service.build_index(st.session_state.recommendations)
            st.session_state.rag_built = True
        except Exception as exc:
            st.info(f"Recommendations unavailable: {exc}")
            return

    recs = st.session_state.recommendations
    agent_filter = st.selectbox("Filter by Agent", ["All"] + sorted({r.get("agent", "Unknown") for r in recs}))
    priority_filter = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])

    for rec in recs:
        if agent_filter != "All" and rec.get("agent") != agent_filter:
            continue
        if priority_filter != "All" and rec.get("priority") != priority_filter:
            continue

        st.markdown(
            f"""
            <div style="background:#151b27;border:1px solid #273042;border-radius:10px;padding:16px;margin-bottom:12px;">
                <div style="color:#93c5fd;font-weight:700;margin-bottom:6px;">{rec.get('agent', 'Unknown')}</div>
                <div style="font-size:1.03rem;margin-bottom:8px;">{rec.get('recommendation', '')}</div>
                <div style="display:flex;justify-content:space-between;color:#9ca3af;">
                    <span>{rec.get('data_point', 'N/A')}</span>
                    <span>{rec.get('priority', 'Low')} Priority</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

