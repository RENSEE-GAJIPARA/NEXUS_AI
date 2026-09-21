"""Streamlit Data Loader with st.cache_data for NEXUS AI."""
import streamlit as st
import pandas as pd
from typing import Dict
from src.data.ingestion import load_canonical_data
from src.data.validation import validate_datasets

@st.cache_data(show_spinner=False)
def get_all_canonical_data() -> Dict[str, pd.DataFrame]:
    """Load and cache canonical business datasets."""
    return load_canonical_data()

@st.cache_data(show_spinner=False)
def get_data_quality_report() -> Dict:
    """Load cached data quality scoring metrics."""
    tables = get_all_canonical_data()
    return validate_datasets(tables)
