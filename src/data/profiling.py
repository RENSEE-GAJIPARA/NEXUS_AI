"""Automated Data Profiling for NEXUS AI."""
import pandas as pd
import numpy as np
from typing import Dict, Any

def profile_dataframe(df: pd.DataFrame, table_name: str) -> Dict[str, Any]:
    """Generate detailed column-level statistical profiling."""
    profile = {
        "table_name": table_name,
        "row_count": len(df),
        "col_count": len(df.columns),
        "columns": {}
    }
    
    for col in df.columns:
        col_series = df[col]
        col_type = str(col_series.dtype)
        null_count = int(col_series.isnull().sum())
        null_pct = round(float(null_count / len(df) * 100), 2) if len(df) > 0 else 0.0
        unique_count = int(col_series.nunique())
        
        col_info = {
            "dtype": col_type,
            "null_count": null_count,
            "null_pct": null_pct,
            "unique_count": unique_count
        }
        
        if np.issubdtype(col_series.dtype, np.number):
            col_info.update({
                "min": round(float(col_series.min()), 2) if not col_series.empty else None,
                "max": round(float(col_series.max()), 2) if not col_series.empty else None,
                "mean": round(float(col_series.mean()), 2) if not col_series.empty else None,
                "std": round(float(col_series.std()), 2) if len(col_series) > 1 else None,
                "median": round(float(col_series.median()), 2) if not col_series.empty else None,
            })
        elif col_series.dtype == "object":
            top_vals = col_series.value_counts().head(3).to_dict()
            col_info["top_categories"] = top_vals
            
        profile["columns"][col] = col_info
        
    return profile
