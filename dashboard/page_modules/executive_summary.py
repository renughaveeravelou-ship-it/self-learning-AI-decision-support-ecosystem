from __future__ import annotations

import streamlit as st


def render() -> None:
    st.title("Executive Summary")

    try:
        from copilot.executive_copilot import executive_summary
        from reporting.monthly_report import generate_monthly_report
        from reporting.report_generator import generate_report
    except Exception as exc:
        st.error(f"Executive tooling is unavailable: {exc}")
        return

    summary = executive_summary()
    st.markdown(summary.replace("\n", "<br/>"), unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Generate Executive PDF Report"):
            pdf_path = generate_report()
            with open(pdf_path, "rb") as handle:
                st.download_button(
                    "Download Executive Report",
                    handle,
                    file_name="Executive_Report.pdf",
                    mime="application/pdf",
                )
    with col2:
        if st.button("Generate Monthly PDF Report"):
            pdf_path = generate_monthly_report()
            with open(pdf_path, "rb") as handle:
                st.download_button(
                    "Download Monthly Report",
                    handle,
                    file_name="Monthly_Report.pdf",
                    mime="application/pdf",
                )

