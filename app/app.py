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
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
css_file = ROOT_PATH / "app" / "styles" / "theme.css"
if css_file.exists():
    with open(css_file, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Imports Pages, Intent Parser & SVG Logo
from app.pages import (
    executive, customers, products, suppliers, graph,
    anomalies, forecasting, scenarios, models, data_quality, about
)
from src.nlp.intent_parser import parse_user_intent
from app.components.nexus_logo import NEXUS_SVG_LOGO

# Header Branding
st.markdown("""
<div class="nexus-header">
    <div class="nexus-title">NEXUS AI</div>
    <div class="nexus-subtitle">Autonomous Graph-Based Business Intelligence & Decision Engine</div>
</div>
""", unsafe_allow_html=True)

# Chatbot Query Panel
st.markdown("""
<div class="nexus-query-panel">
    <div class="nexus-query-title">Ask NEXUS AI</div>
    <div class="nexus-query-subtitle">Ask questions about customers, suppliers, products, forecasts, risks, anomalies, and business performance.</div>
</div>
""", unsafe_allow_html=True)

# Query Input & Submit Button
query_col, btn_col = st.columns([4, 1])
with query_col:
    nlp_query = st.text_input(
        "Ask NEXUS AI Query Input",
        placeholder="Ask a business question, for example: Show me high-risk suppliers",
        label_visibility="collapsed",
        key="query_input_text"
    )
with btn_col:
    submit_btn = st.button("Ask NEXUS AI", use_container_width=True, type="primary")

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

clean_pages = list(pages_map.keys())

# Intent Query Processing
if "selected_page" not in st.session_state:
    st.session_state["selected_page"] = "Executive Overview"

query_to_process = nlp_query if submit_btn or nlp_query else None
if query_to_process and query_to_process.strip():
    parsed = parse_user_intent(query_to_process)
    target = parsed.get("target_page", "Executive Overview")
    if target in pages_map:
        st.session_state["selected_page"] = target
    
    st.markdown(f"""
    <div style="background-color: #FFFFFF; border: 1px solid #2563EB; border-radius: 8px; padding: 14px 18px; margin-bottom: 20px;">
        <div style="font-size: 0.85rem; font-weight: 600; color: #5F6B7A; text-transform: uppercase;">User Query</div>
        <div style="font-size: 1.05rem; font-weight: 600; color: #172033; margin-bottom: 8px;">"{query_to_process}"</div>
        <div style="font-size: 0.85rem; font-weight: 600; color: #2563EB;">NEXUS AI Analysis</div>
        <div style="font-size: 0.9rem; color: #5F6B7A;">Matched Intent: <strong>{parsed['intent']}</strong> (Confidence: {parsed['confidence']:.0%}) &mdash; Routing to <strong>{target}</strong></div>
    </div>
    """, unsafe_allow_html=True)

# Sidebar Branding & Navigation
st.sidebar.markdown(f"""
<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 6px;">
    {NEXUS_SVG_LOGO}
    <div>
        <div class="sidebar-brand-title" style="margin:0;">NEXUS AI</div>
    </div>
</div>
<div class="sidebar-brand-sub">Autonomous Graph-Based Business Intelligence & Decision Engine</div>
<hr style="margin: 12px 0; border: none; border-top: 1px solid #D9E0E8;"/>
<div class="sidebar-section-header">Platform Navigation</div>
""", unsafe_allow_html=True)

# Set index for radio selection
curr_idx = clean_pages.index(st.session_state["selected_page"]) if st.session_state["selected_page"] in clean_pages else 0
selected_nav = st.sidebar.radio("Platform Navigation:", clean_pages, index=curr_idx, label_visibility="collapsed")
st.session_state["selected_page"] = selected_nav

# Render Page
module = pages_map.get(selected_nav)
if module:
    module.render()
else:
    st.error("Page not found.")

