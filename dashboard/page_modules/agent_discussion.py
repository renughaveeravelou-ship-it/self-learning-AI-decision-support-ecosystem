from __future__ import annotations

import streamlit as st


def render() -> None:
    st.title("Agent Discussion")

    try:
        from collaboration.agent_discussion import run_discussion
    except Exception as exc:
        st.error(f"Agent discussion module unavailable: {exc}")
        return

    discussion = run_discussion()
    for name, item in discussion.items():
        payload = item if isinstance(item, dict) else {"agent": name, "message": str(item), "priority": "LOW"}
        st.markdown(
            f"**{payload.get('agent', name)}**  \nPriority: {payload.get('priority', 'LOW')}  \n{payload.get('message', payload)}"
        )

