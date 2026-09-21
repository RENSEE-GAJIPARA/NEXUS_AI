"""Isolation Forest Anomaly Detection Engine for NEXUS AI."""
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from src.features.transaction_features import build_transaction_features
from src.models.registry import save_model_artifact, load_model_artifact
from src.utils.logging import logger

ANOMALY_FEATURE_COLS = ["total_amount", "total_items", "max_discount", "avg_item_price"]

def train_anomaly_model(df_transactions: pd.DataFrame, df_tx_items: pd.DataFrame, contamination: float = 0.03):
    """Train Isolation Forest anomaly detector on transaction features."""
    df_feat = build_transaction_features(df_transactions, df_tx_items)
    if df_feat.empty:
        return None
        
    X = df_feat[ANOMALY_FEATURE_COLS].fillna(0)
    
    iso_model = IsolationForest(contamination=contamination, random_state=42, n_estimators=100)
    iso_model.fit(X)
    
    metadata = {
        "algorithm": "IsolationForest",
        "contamination": contamination,
        "features": ANOMALY_FEATURE_COLS,
        "dataset_rows": len(df_feat)
    }
    save_model_artifact("anomaly_model", iso_model, metadata)
    return iso_model

def detect_transaction_anomalies(df_transactions: pd.DataFrame, df_tx_items: pd.DataFrame) -> pd.DataFrame:
    """Detect anomalies in transactions and attach anomaly score and explanations."""
    df_feat = build_transaction_features(df_transactions, df_tx_items)
    model, metadata = load_model_artifact("anomaly_model")
    
    if model is None:
        model = train_anomaly_model(df_transactions, df_tx_items)
        
    X = df_feat[ANOMALY_FEATURE_COLS].fillna(0)
    
    # Isolation Forest score_samples returns negative anomaly score (lower means more anomalous)
    raw_scores = model.score_samples(X)
    # Normalize score to 0 to 1 range (higher = more anomalous)
    norm_scores = 1.0 - (raw_scores - raw_scores.min()) / (raw_scores.max() - raw_scores.min() + 1e-6)
    
    preds = model.predict(X) # -1 for anomaly, 1 for normal
    
    df_res = df_feat[["transaction_id", "customer_id", "store_id", "transaction_date", "total_amount", "total_items", "max_discount"]].copy()
    df_res["anomaly_score"] = round(pd.Series(norm_scores, index=df_res.index), 4)
    df_res["is_anomaly"] = (preds == -1).astype(int)
    
    # Generate explanations for flagged anomalies
    df_res["anomaly_explanation"] = df_res.apply(generate_anomaly_reason, axis=1)
    
    return df_res

def generate_anomaly_reason(row: pd.Series) -> str:
    """Generate empirical explanation for an anomalous transaction."""
    if row["is_anomaly"] == 0:
        return "Normal Transaction Pattern"
        
    reasons = []
    if row["total_amount"] > 1500:
        reasons.append(f"Unusually high transaction total (${row['total_amount']:,.2f})")
    if row["total_items"] > 15:
        reasons.append(f"Excessive item volume ({row['total_items']} items)")
    if row["max_discount"] >= 0.50:
        reasons.append(f"Extremely high discount rate ({row['max_discount']:.0%})")
        
    if not reasons:
        reasons.append("Multi-variable statistical deviation from baseline profile")
        
    return "Potential anomaly requiring investigation: " + "; ".join(reasons) + "."
