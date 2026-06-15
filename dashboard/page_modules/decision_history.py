from __future__ import annotations

import streamlit as st


def render() -> None:
    st.title("Decision History")

    try:
        from memory.decision_memory import get_decision_history, save_decision
    except Exception as exc:
        st.error(f"Decision history module unavailable: {exc}")
        return

    history = get_decision_history()
    if not history.empty:
        st.dataframe(history, use_container_width=True)
    else:
        st.info("No decisions recorded yet.")

    with st.form("new_decision"):
        decision = st.text_input("Decision details")
        outcome = st.selectbox("Outcome", ["success", "pending", "failed"])
        confidence = st.slider("Confidence", 0, 100, 85)
        submitted = st.form_submit_button("Record")
        if submitted and decision:
            save_decision(decision, outcome, confidence)
            st.success("Decision saved.")

