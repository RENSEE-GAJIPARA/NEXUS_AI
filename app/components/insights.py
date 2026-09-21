"""Insight Callouts and Disclaimer Banners for NEXUS AI."""
import streamlit as st

def render_insight_box(title: str, text: str, icon: str = ""):
    """Render styled analytical insight callout."""
    prefix = f"{icon} " if icon and not any(ord(c) > 0x2000 for c in icon) else ""
    st.info(f"**{prefix}{title}**\n\n{text}")

def render_methodology_disclaimer(message: str = None):
    """Render standard methodology disclaimer."""
    msg = message or (
        "NEXUS AI provides analytical decision support based on statistical machine learning models. "
        "Outputs represent estimates derived from available historical data and should not be treated as guaranteed real-world outcomes."
    )
    st.caption(f"**Methodology Disclaimer:** {msg}")

