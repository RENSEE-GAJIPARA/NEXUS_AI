"""Streamlit Resource Loader with st.cache_resource for NEXUS AI."""
import streamlit as st
import joblib
import pandas as pd
from typing import Dict, Any, Tuple
from src.utils.paths import MODELS_DIR
from src.models.registry import load_model_artifact

@st.cache_resource(show_spinner=False)
def get_model_and_metadata(model_name: str) -> Tuple[Any, Dict]:
    """Load cached model artifact and JSON metadata."""
    return load_model_artifact(model_name)

@st.cache_resource(show_spinner=False)
def get_business_graph():
    """Load cached NetworkX business graph artifact."""
    graph_path = MODELS_DIR / "business_graph.joblib"
    if graph_path.exists():
        return joblib.load(graph_path)
    return None
