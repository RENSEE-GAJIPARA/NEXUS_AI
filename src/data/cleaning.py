"""Data cleaning and standardizing pipeline for NEXUS AI."""
import pandas as pd

def clean_canonical_tables(tables: dict) -> dict:
    """Clean and standardize data across all canonical tables."""
    cleaned = {}
    for name, df in tables.items():
        if df.empty:
            cleaned[name] = df
            continue
        df_clean = df.copy()
        
        # Drop exact duplicate rows
        df_clean = df_clean.drop_duplicates()
        
        # Standardize strings
        for col in df_clean.select_dtypes(include="object").columns:
            if "date" not in col and "id" not in col:
                df_clean[col] = df_clean[col].astype(str).str.strip()
                
        cleaned[name] = df_clean
    return cleaned
