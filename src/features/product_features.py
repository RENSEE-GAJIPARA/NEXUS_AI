"""Product Feature Engineering for NEXUS AI."""
import pandas as pd
import numpy as np

def build_product_features(df_products: pd.DataFrame, df_tx_items: pd.DataFrame, df_transactions: pd.DataFrame) -> pd.DataFrame:
    """Calculate product sales velocity, revenue contribution, and customer reach."""
    if df_products.empty or df_tx_items.empty:
        return pd.DataFrame()
        
    merged = df_tx_items.merge(df_transactions[["transaction_id", "customer_id", "store_id", "transaction_date"]], on="transaction_id", how="left")
    
    prod_agg = merged.groupby("product_id").agg(
        total_units_sold=("quantity", "sum"),
        total_revenue=("item_total", "sum"),
        avg_discount=("discount", "mean"),
        unique_customers=("customer_id", "nunique"),
        unique_stores=("store_id", "nunique")
    ).reset_index()
    
    features = df_products.merge(prod_agg, on="product_id", how="left")
    features["total_units_sold"] = features["total_units_sold"].fillna(0)
    features["total_revenue"] = features["total_revenue"].fillna(0.0)
    features["avg_discount"] = features["avg_discount"].fillna(0.0)
    features["unique_customers"] = features["unique_customers"].fillna(0)
    features["unique_stores"] = features["unique_stores"].fillna(0)
    
    # Margin calculation
    features["gross_margin"] = (features["unit_price"] - features["unit_cost"]) / features["unit_price"]
    
    return features
