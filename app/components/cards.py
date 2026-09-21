"""KPI Metric Card Component for NEXUS AI."""
import streamlit as st

def render_kpi_card(title: str, value: str, subtitle: str = "", border_color: str = "#2563EB"):
    """Render custom html metric card."""
    html_content = f"""
    <div class="nexus-card" style="border-left: 4px solid {border_color};">
        <div class="nexus-card-title">{title}</div>
        <div class="nexus-card-value">{value}</div>
        {f'<div class="nexus-card-subtitle">{subtitle}</div>' if subtitle else ''}
    </div>
    """
    st.markdown(html_content, unsafe_allow_html=True)

def render_risk_badge(risk_level: str) -> str:
    """Return HTML string for styled risk level badge."""
    level = str(risk_level).lower()
    if level == "high":
        return '<span class="badge-high">HIGH RISK</span>'
    elif level == "medium":
        return '<span class="badge-medium">MEDIUM RISK</span>'
    else:
        return '<span class="badge-low">LOW RISK</span>'

