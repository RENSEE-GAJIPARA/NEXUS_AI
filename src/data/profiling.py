"""Automated Data Profiling for NEXUS AI."""
import pandas as pd
import numpy as np
from typing import Dict, Any
from pandas.api.types import (
    is_numeric_dtype,
    is_bool_dtype,
    is_datetime64_any_dtype,
    is_categorical_dtype,
    is_string_dtype,
    is_object_dtype
)

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
        
        valid_series = col_series.dropna()
        
        if is_numeric_dtype(col_series) and not is_bool_dtype(col_series):
            if not valid_series.empty:
                try:
                    c_min = float(valid_series.min())
                    c_max = float(valid_series.max())
                    c_mean = float(valid_series.mean())
                    c_median = float(valid_series.median())
                    c_std = float(valid_series.std()) if len(valid_series) > 1 else None
                    
                    col_info.update({
                        "min": round(c_min, 2) if not np.isnan(c_min) else None,
                        "max": round(c_max, 2) if not np.isnan(c_max) else None,
                        "mean": round(c_mean, 2) if not np.isnan(c_mean) else None,
                        "std": round(c_std, 2) if c_std is not None and not np.isnan(c_std) else None,
                        "median": round(c_median, 2) if not np.isnan(c_median) else None,
                    })
                except Exception:
                    pass
        elif is_datetime64_any_dtype(col_series):
            if not valid_series.empty:
                col_info["min_date"] = str(valid_series.min())
                col_info["max_date"] = str(valid_series.max())
        elif is_object_dtype(col_series) or is_string_dtype(col_series) or is_categorical_dtype(col_series) or is_bool_dtype(col_series):
            if not valid_series.empty:
                top_vals = valid_series.astype(str).value_counts().head(3).to_dict()
                col_info["top_categories"] = str(top_vals)
            else:
                col_info["top_categories"] = "{}"
            
        profile["columns"][col] = col_info
        
    return profile

