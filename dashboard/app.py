from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from dashboard.core import ensure_project_root, init_session_state
from dashboard.page_modules.agent_discussion import render as render_agent_discussion
from dashboard.page_modules.ai_copilot import render as render_ai_copilot
from dashboard.page_modules.control_center import render as render_control_center
from dashboard.page_modules.decision_history import render as render_decision_history
from dashboard.page_modules.decision_support import render as render_decision_support
from dashboard.page_modules.drift_detector import render as render_drift_detector
from dashboard.page_modules.enterprise_kpi import render as render_enterprise_kpi
from dashboard.page_modules.executive_summary import render as render_executive_summary
from dashboard.page_modules.feedback_analytics import render as render_feedback_analytics
from dashboard.page_modules.overview import render as render_overview
from dashboard.page_modules.rag_assistant import render as render_rag_assistant
from dashboard.page_modules.recommendations import render as render_recommendations
from dashboard.page_modules.shap_explainability import render as render_shap_explainability

ensure_project_root()

st.set_page_config(
    page_title="Self-Learning AI Decision Support Ecosystem",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        .stApp { background: #0f1117; color: #e5e7eb; }
        [data-testid="stSidebar"] { background: #141824; }
        .app-header {
            padding: 1.1rem 1.2rem;
            border: 1px solid #2a2f3a;
            border-radius: 12px;
            background: linear-gradient(135deg, #161b2a 0%, #111827 100%);
            margin-bottom: 1rem;
        }
        .app-title { font-size: 1.8rem; font-weight: 700; margin: 0; }
        .app-subtitle { color: #9ca3af; margin-top: 0.25rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

init_session_state()

st.markdown(
    """
    <div class="app-header">
        <div class="app-title">Self-Learning AI Decision Support Ecosystem</div>
        <div class="app-subtitle">Single-entry Streamlit dashboard with sidebar dropdown navigation</div>
    </div>
    """,
    unsafe_allow_html=True,
)

pages = {
    "Overview Dashboard": render_overview,
    "Decision Support Desk": render_decision_support,
    "AI RAG Assistant": render_rag_assistant,
    "Control Center": render_control_center,
    "Enterprise KPI Dashboard": render_enterprise_kpi,
    "Executive Summary": render_executive_summary,
    "AI Copilot": render_ai_copilot,
    "Recommendations": render_recommendations,
    "Feedback Analytics": render_feedback_analytics,
    "Agent Discussion": render_agent_discussion,
    "Decision History": render_decision_history,
    "Drift Detector": render_drift_detector,
    "SHAP Explainability": render_shap_explainability,
}

selected_page = st.sidebar.selectbox("Navigation", list(pages.keys()))
pages[selected_page]()
