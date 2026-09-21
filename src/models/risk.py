"""Customer Risk & Churn Prediction Model for NEXUS AI."""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

from src.models.evaluation import evaluate_classification
from src.models.registry import save_model_artifact, load_model_artifact
from src.features.customer_features import build_customer_features
from src.utils.logging import logger

FEATURE_COLS = ["age", "recency_days", "frequency", "monetary_total", "avg_order_value", "product_diversity", "tenure_days"]

def train_customer_risk_model(df_customers: pd.DataFrame, df_transactions: pd.DataFrame, df_tx_items: pd.DataFrame):
    """Train baseline & candidate classifiers for proxy customer churn risk."""
    df_feat = build_customer_features(df_customers, df_transactions, df_tx_items)
    if df_feat.empty or "proxy_churn" not in df_feat.columns:
        logger.error("Empty features for customer risk model.")
        return None
        
    X = df_feat[FEATURE_COLS].fillna(0)
    y = df_feat["proxy_churn"]
    
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    
    # Candidates
    candidates = {
        "Dummy": DummyClassifier(strategy="prior"),
        "LogisticRegression": LogisticRegression(max_iter=1000, random_state=42),
        "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42),
        "GradientBoosting": GradientBoostingClassifier(n_estimators=100, random_state=42)
    }
    
    best_model = None
    best_name = ""
    best_metrics = {"f1": -1.0}
    comparison = {}
    
    for name, model in candidates.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_val)
        probs = model.predict_proba(X_val)[:, 1] if hasattr(model, "predict_proba") else None
        
        metrics = evaluate_classification(y_val, preds, probs)
        comparison[name] = metrics
        logger.info(f"Model '{name}' -> F1: {metrics['f1']}, ROC-AUC: {metrics.get('roc_auc')}")
        
        if metrics["f1"] > best_metrics["f1"]:
            best_metrics = metrics
            best_model = model
            best_name = name
            
    # Save winner to artifact registry
    metadata = {
        "target": "proxy_churn",
        "features": FEATURE_COLS,
        "algorithm": best_name,
        "metrics": best_metrics,
        "all_candidate_metrics": comparison,
        "dataset_rows": len(df_feat)
    }
    save_model_artifact("customer_risk_model", best_model, metadata)
    return best_model

def predict_customer_risk(df_customers: pd.DataFrame, df_transactions: pd.DataFrame, df_tx_items: pd.DataFrame) -> pd.DataFrame:
    """Run inference using saved customer risk artifact."""
    df_feat = build_customer_features(df_customers, df_transactions, df_tx_items)
    model, metadata = load_model_artifact("customer_risk_model")
    
    if model is None:
        logger.warning("No saved customer risk model found. Training on the fly...")
        model = train_customer_risk_model(df_customers, df_transactions, df_tx_items)
        
    X = df_feat[FEATURE_COLS].fillna(0)
    probs = model.predict_proba(X)[:, 1]
    
    results = df_feat[["customer_id", "recency_days", "frequency", "monetary_total"]].copy()
    results["risk_probability"] = round(pd.Series(probs, index=results.index), 4)
    
    # Assign risk bands
    conditions = [
        (results["risk_probability"] >= 0.70),
        (results["risk_probability"] >= 0.40) & (results["risk_probability"] < 0.70),
        (results["risk_probability"] < 0.40)
    ]
    bands = ["High", "Medium", "Low"]
    results["risk_band"] = np.select(conditions, bands, default="Low")
    
    return results
