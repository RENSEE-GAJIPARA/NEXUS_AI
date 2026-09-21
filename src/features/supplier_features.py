"""Supplier Feature Engineering for NEXUS AI."""
import pandas as pd
import numpy as np

def build_supplier_features(df_suppliers: pd.DataFrame, df_products: pd.DataFrame, df_tx_items: pd.DataFrame) -> pd.DataFrame:
    """Calculate supplier dependency, product count, and revenue risk exposure."""
    if df_suppliers.empty or df_products.empty:
        return pd.DataFrame()
        
    prod_sup = df_products.merge(df_tx_items, on="product_id", how="left")
    
    sup_agg = prod_sup.groupby("supplier_id").agg(
        num_products=("product_id", "nunique"),
        total_units_supplied=("quantity", "sum"),
        total_revenue_exposure=("item_total", "sum")
    ).reset_index()
    
    features = df_suppliers.merge(sup_agg, on="supplier_id", how="left")
    features["num_products"] = features["num_products"].fillna(0)
    features["total_units_supplied"] = features["total_units_supplied"].fillna(0)
    features["total_revenue_exposure"] = features["total_revenue_exposure"].fillna(0.0)
    
    # Calculate composite risk score: Delay Rate * (1.0 - Reliability) * Exposure Factor
    max_rev = features["total_revenue_exposure"].max() or 1.0
    features["revenue_concentration"] = features["total_revenue_exposure"] / max_rev
    features["composite_supplier_risk"] = (
        0.4 * features["delay_rate"] + 
        0.4 * (1.0 - features["reliability_score"]) + 
        0.2 * features["revenue_concentration"]
    ).clip(0.0, 1.0)
    
    return features
