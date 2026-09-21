"""NEXUS AI — Main Streamlit Application Entrypoint."""
import sys
import os
from pathlib import Path

# Ensure root directory is in sys.path
ROOT_PATH = Path(__file__).resolve().parents[1]
if str(ROOT_PATH) not in sys.path:
    sys.path.insert(0, str(ROOT_PATH))

import streamlit as st

# Configure Page
st.set_page_config(
    page_title="NEXUS AI — Business Intelligence Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
css_file = ROOT_PATH / "app" / "styles" / "theme.css"
if css_file.exists():
    with open(css_file, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Imports Pages & Intent Parser
from app.pages import (
    executive, customers, products, suppliers, graph,
    anomalies, forecasting, scenarios, models, data_quality, about
)
from src.nlp.intent_parser import parse_user_intent

# Header Branding
st.markdown("""
<div class="nexus-header">
    <div class="nexus-title">NEXUS AI</div>
    <div class="nexus-subtitle">Autonomous Graph-Based Business Intelligence & Decision Engine</div>
</div>
""", unsafe_allow_html=True)

# Top Bar Natural Language Search Input (Zero-Paid API Intent Engine)
nlp_query = st.text_input("💬 Ask NEXUS AI a Natural Language Query:", placeholder="e.g. 'Show me high risk suppliers', 'Which customers are at risk of churn?', 'Predict revenue next 14 days'")

detected_page = None
if nlp_query:
    parsed = parse_user_intent(nlp_query)
    detected_page = parsed["target_page"]
    st.toast(f"Parsed Intent: {parsed['intent']} (Routing to '{detected_page}')", icon="💡")

# Sidebar Navigation
st.sidebar.image("https://img.icons8.com/color/96/000000/artificial-intelligence.png", width=64)
st.sidebar.title("NEXUS AI Platform")

pages_map = {
    "Executive Overview": executive,
    "Customer Intelligence": customers,
    "Product Intelligence": products,
    "Supplier Intelligence": suppliers,
    "Graph Intelligence": graph,
    "Anomaly Detection": anomalies,
    "Forecast Center": forecasting,
    "Scenario Lab": scenarios,
    "Model Center": models,
    "Data Quality": data_quality,
    "About / Methodology": about
}

page_icons = [
    "📊 Executive Overview",
    "👤 Customer Intelligence",
    "📦 Product Intelligence",
    "🏭 Supplier Intelligence",
    "🕸️ Graph Intelligence",
    "🚨 Anomaly Detection",
    "📈 Forecast Center",
    "🎛️ Scenario Lab",
    "🤖 Model Center",
    "🛡️ Data Quality",
    "📖 About / Methodology"
]

default_idx = 0
if detected_page:
    for idx, icon_name in enumerate(page_icons):
        if detected_page in icon_name:
            default_idx = idx
            break

selected_page_icon = st.sidebar.radio("Platform Navigation:", page_icons, index=default_idx)

# Extract clean page title
clean_page_name = selected_page_icon.split(" ", 1)[1]

# Render Page
module = pages_map.get(clean_page_name)
if module:
    module.render()
else:
    st.error("Page not found.")
