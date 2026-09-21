"""Transaction Feature Engineering for NEXUS AI."""
import pandas as pd
import numpy as np

def build_transaction_features(df_transactions: pd.DataFrame, df_tx_items: pd.DataFrame) -> pd.DataFrame:
    """Engineer item count, average discount, and temporal markers for transactions."""
    if df_transactions.empty:
        return pd.DataFrame()
        
    tx_df = df_transactions.copy()
    tx_df["transaction_date"] = pd.to_datetime(tx_df["transaction_date"])
    
    item_agg = df_tx_items.groupby("transaction_id").agg(
        total_items=("quantity", "sum"),
        item_count=("product_id", "nunique"),
        avg_item_price=("unit_price", "mean"),
        max_discount=("discount", "max")
    ).reset_index()
    
    features = tx_df.merge(item_agg, on="transaction_id", how="left")
    features["total_items"] = features["total_items"].fillna(1)
    features["item_count"] = features["item_count"].fillna(1)
    features["avg_item_price"] = features["avg_item_price"].fillna(features["total_amount"])
    features["max_discount"] = features["max_discount"].fillna(0.0)
    
    features["day_of_week"] = features["transaction_date"].dt.dayofweek
    features["is_weekend"] = (features["day_of_week"] >= 5).astype(int)
    features["month"] = features["transaction_date"].dt.month
    
    return features
