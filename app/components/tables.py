"""Table formatting utilities for NEXUS AI."""
import streamlit as st
import pandas as pd

def render_data_table(df: pd.DataFrame, height: int = 350):
    """Render clean, searchable Streamlit dataframe table."""
    st.dataframe(
        df,
        use_container_width=True,
        height=height,
        hide_index=True
    )
