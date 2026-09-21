"""Evaluation metrics for classification, regression, and forecasting in NEXUS AI."""
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score, confusion_matrix,
    mean_absolute_error, mean_squared_error, r2_score
)
from typing import Dict, Any

def evaluate_classification(y_true, y_pred, y_prob=None) -> Dict[str, Any]:
    """Calculate comprehensive classification metrics."""
    metrics = {
        "accuracy": round(float(accuracy_score(y_true, y_pred)), 4),
        "precision": round(float(precision_score(y_true, y_pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_true, y_pred, zero_division=0)), 4),
        "f1": round(float(f1_score(y_true, y_pred, zero_division=0)), 4),
    }
    if y_prob is not None:
        try:
            metrics["roc_auc"] = round(float(roc_auc_score(y_true, y_prob)), 4)
            metrics["pr_auc"] = round(float(average_precision_score(y_true, y_prob)), 4)
        except Exception:
            metrics["roc_auc"] = None
            metrics["pr_auc"] = None
    return metrics

def evaluate_regression(y_true, y_pred) -> Dict[str, Any]:
    """Calculate regression / forecasting metrics."""
    mae = float(mean_absolute_error(y_true, y_pred))
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    r2 = float(r2_score(y_true, y_pred))
    
    # Calculate SMAPE (Symmetric Mean Absolute Percentage Error)
    denominator = (np.abs(y_true) + np.abs(y_pred)) / 2.0
    smape = float(np.mean(np.where(denominator == 0, 0, np.abs(y_pred - y_true) / denominator)) * 100)
    
    return {
        "mae": round(mae, 2),
        "rmse": round(rmse, 2),
        "r2": round(r2, 4),
        "smape": round(smape, 2)
    }
