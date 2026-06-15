from __future__ import annotations

import streamlit as st


def render() -> None:
    st.title("AI Copilot")
    query = st.text_input("Ask a question about the business")
    if not query:
        return

    try:
        from llm.executive_assistant import ask_copilot
    except Exception as exc:
        st.error(f"Copilot is unavailable: {exc}")
        return

    with st.spinner("Generating answer..."):
        st.markdown(ask_copilot(query))

