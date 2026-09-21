"""Anomaly Detection Page for NEXUS AI."""
import streamlit as st
import pandas as pd
from app.utils.data_loader import get_all_canonical_data
from app.components.cards import render_kpi_card
from app.components.charts import plot_bar_chart
from app.components.tables import render_data_table
from app.components.insights import render_methodology_disclaimer
from src.anomaly.isolation_forest import detect_transaction_anomalies

def render():
    st.header("Multi-Dimensional Anomaly Detection")
    st.markdown("Isolation Forest unsupervised outlier scoring on transaction volume, quantities, and discount rates.")
    
    tables = get_all_canonical_data()
    df_tx = tables.get("transactions", pd.DataFrame())
    df_items = tables.get("transaction_items", pd.DataFrame())
    
    if df_tx.empty:
        st.warning("Transaction data unavailable.")
        return
        
    df_ano = detect_transaction_anomalies(df_tx, df_items)
    flagged = df_ano[df_ano["is_anomaly"] == 1].sort_values(by="anomaly_score", ascending=False)
    
    num_flagged = len(flagged)
    ano_rate = num_flagged / len(df_tx) if len(df_tx) > 0 else 0.0
    
    c1, c2, c3 = st.columns(3)
    with c1:
        render_kpi_card("Total Flagged Anomalies", f"{num_flagged:,}", f"Out of {len(df_tx):,} Transactions", "#DC2626")
    with c2:
        render_kpi_card("Anomaly Rate", f"{ano_rate:.2%}", "Contamination Target 3.0%", "#D97706")
    with c3:
        render_kpi_card("Highest Anomaly Score", f"{flagged['anomaly_score'].max() if not flagged.empty else 0.0:.4f}", "Isolation Forest Score", "#2563EB")
        
    st.markdown("---")
    st.subheader("Flagged Transactions Requiring Investigation")
    desired_cols = ["transaction_id", "customer_id", "store_id", "transaction_date", "total_amount", "total_items", "max_discount", "anomaly_score", "anomaly_explanation"]
    avail_cols = [c for c in desired_cols if c in flagged.columns]
    render_data_table(flagged[avail_cols])
    
    render_methodology_disclaimer("Anomaly detection identifies statistical multi-variable outliers. Flagged records indicate unusual transaction characteristics and do not automatically constitute verified fraud.")

