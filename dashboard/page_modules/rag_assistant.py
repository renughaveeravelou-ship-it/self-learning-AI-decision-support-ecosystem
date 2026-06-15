from __future__ import annotations

import streamlit as st

from dashboard.core import init_session_state


def render() -> None:
    init_session_state()
    st.title("AI RAG Assistant")
    st.caption("Semantic search over live recommendations and dataset summaries.")

    if st.session_state.recommendations and not st.session_state.rag_built:
        st.session_state.rag_service.build_index(st.session_state.recommendations)
        st.session_state.rag_built = True

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask a question")
    if not prompt:
        return

    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Searching..."):
            answer = st.session_state.rag_service.query(prompt)
            st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})

