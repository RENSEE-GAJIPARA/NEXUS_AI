"""Customer Feature Engineering for NEXUS AI."""
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict

def build_customer_features(df_customers: pd.DataFrame, df_transactions: pd.DataFrame, df_tx_items: pd.DataFrame, ref_date_str: str = "2025-12-31") -> pd.DataFrame:
    """Compute Recency, Frequency, Monetary (RFM), diversity, and proxy churn target."""
    if df_customers.empty or df_transactions.empty:
        return pd.DataFrame()
        
    ref_date = pd.to_datetime(ref_date_str)
    tx_df = df_transactions.copy()
    tx_df["transaction_date"] = pd.to_datetime(tx_df["transaction_date"])
    
    # Merge items to calculate category diversity & total quantity
    tx_merged = tx_df.merge(df_tx_items, on="transaction_id", how="left")
    
    # Customer level aggregates
    cust_agg = tx_df.groupby("customer_id").agg(
        last_purchase_date=("transaction_date", "max"),
        first_purchase_date=("transaction_date", "min"),
        frequency=("transaction_id", "nunique"),
        monetary_total=("total_amount", "sum"),
        avg_order_value=("total_amount", "mean")
    ).reset_index()
    
    # Merge category diversity
    diversity = tx_merged.groupby("customer_id")["product_id"].nunique().reset_index().rename(columns={"product_id": "product_diversity"})
    cust_agg = cust_agg.merge(diversity, on="customer_id", how="left")
    
    # Calculate RFM metrics
    cust_agg["recency_days"] = (ref_date - cust_agg["last_purchase_date"]).dt.days
    cust_agg["tenure_days"] = (ref_date - cust_agg["first_purchase_date"]).dt.days
    
    # Merge back into customer base
    features = df_customers.merge(cust_agg, on="customer_id", how="left")
    features["recency_days"] = features["recency_days"].fillna(365)
    features["frequency"] = features["frequency"].fillna(0)
    features["monetary_total"] = features["monetary_total"].fillna(0.0)
    features["avg_order_value"] = features["avg_order_value"].fillna(0.0)
    features["product_diversity"] = features["product_diversity"].fillna(0)

    # Proxy Churn Target: Inactivity > 60 days
    features["proxy_churn"] = (features["recency_days"] > 60).astype(int)
    
    return features
