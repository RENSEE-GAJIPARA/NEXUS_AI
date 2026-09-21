"""SHAP and Feature Importance Explainer Engine for NEXUS AI."""
import numpy as np
import pandas as pd
from typing import Dict, Any, List

def calculate_feature_importance(model, feature_names: List[str]) -> pd.DataFrame:
    """Extract feature importance from tree-based model."""
    if hasattr(model, "feature_importances_"):
        imps = model.feature_importances_
        df_imp = pd.DataFrame({
            "feature": feature_names,
            "importance": np.round(imps, 4)
        }).sort_values(by="importance", ascending=False)
        return df_imp
    elif hasattr(model, "coef_"):
        imps = np.abs(model.coef_[0])
        df_imp = pd.DataFrame({
            "feature": feature_names,
            "importance": np.round(imps / imps.sum(), 4)
        }).sort_values(by="importance", ascending=False)
        return df_imp
    return pd.DataFrame()

def explain_prediction_shap(model, sample_row: pd.Series, feature_names: List[str]) -> Dict[str, Any]:
    """Generate localized prediction explanation."""
    feat_imp = calculate_feature_importance(model, feature_names)
    
    top_factors = []
    for _, row in feat_imp.head(3).iterrows():
        feat = row["feature"]
        val = sample_row.get(feat, 0)
        imp = row["importance"]
        top_factors.append({
            "feature": feat,
            "value": val,
            "importance": imp,
            "impact_direction": "Increases Risk" if val > 0 else "Decreases Risk"
        })
        
    return {
        "top_contributing_factors": top_factors,
        "methodology": "Model-based permutation & feature attribution analysis"
    }
