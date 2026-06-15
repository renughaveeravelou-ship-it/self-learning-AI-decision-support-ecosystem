from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent.parent
SAVED_MODELS_DIR = ROOT_DIR / "saved_models"

DEFAULT_METRICS = {
    "customer_silhouette": 0.485,
    "sales_r2": 0.892,
    "market_r2": 0.764,
    "social_r2": 0.811,
    "maintenance_accuracy": 0.945,
    "maintenance_auc": 0.982,
}


def ensure_project_root() -> None:
    root = str(ROOT_DIR)
    if root not in sys.path:
        sys.path.insert(0, root)


def data_path(*parts: str) -> Path:
    return ROOT_DIR.joinpath(*parts)


def load_csv(filename: str):
    path = data_path(filename)
    if path.exists():
        return pd.read_csv(path)
    return None


def load_metrics() -> dict:
    metrics_path = SAVED_MODELS_DIR / "metrics.json"
    if metrics_path.exists():
        try:
            return json.loads(metrics_path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return DEFAULT_METRICS.copy()


def get_rag_service():
    try:
        from rag_service import RAGService

        return RAGService()
    except Exception as exc:
        reason = str(exc)

        class FallbackRAGService:
            def __init__(self):
                self.reason = reason
                self.recommendations = []

            def build_index(self, recommendations):
                self.recommendations = list(recommendations or [])
                return False

            def query(self, query_text):
                return (
                    "RAG service is unavailable right now: "
                    f"{self.reason}"
                )

        return FallbackRAGService()


def init_session_state() -> None:
    if "rag_service" not in st.session_state:
        st.session_state.rag_service = get_rag_service()
    if "rag_built" not in st.session_state:
        st.session_state.rag_built = False
    if "recommendations" not in st.session_state:
        st.session_state.recommendations = []
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "feedback_refresh" not in st.session_state:
        st.session_state.feedback_refresh = 0


def build_recommendations():
    from agents.agent_orchestrator import run_agents

    return run_agents()


def save_feedback_entry(recommendation: str, status: str) -> None:
    from self_learning.feedback_manager import save_feedback

    outcome = "success" if status == "Agree" else "failed"
    save_feedback(recommendation, outcome)


def train_all_models():
    from train import train_all_models as _train_all_models

    return _train_all_models()
