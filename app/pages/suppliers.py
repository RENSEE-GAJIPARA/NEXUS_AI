"""Supplier Intelligence Page for NEXUS AI."""
import streamlit as st
import pandas as pd
from app.utils.data_loader import get_all_canonical_data
from app.components.cards import render_kpi_card
from app.components.charts import plot_bar_chart
from app.components.tables import render_data_table
from app.components.insights import render_insight_box
from src.features.supplier_features import build_supplier_features
from src.utils.insights import generate_supplier_risk_insight

def render():
    st.header("Supplier Intelligence & Risk Analytics")
    st.markdown("Operational reliability, delivery delay rates, vulnerability exposure, and composite risk scoring.")
    
    tables = get_all_canonical_data()
    df_sup = tables.get("suppliers", pd.DataFrame())
    df_prod = tables.get("products", pd.DataFrame())
    df_items = tables.get("transaction_items", pd.DataFrame())
    
    if df_sup.empty:
        st.warning("Supplier data unavailable.")
        return
        
    sup_feat = build_supplier_features(df_sup, df_prod, df_items)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("High-Risk Suppliers")
        high_sup = sup_feat.sort_values(by="composite_supplier_risk", ascending=False).head(5)
        for _, row in high_sup.iterrows():
            render_kpi_card(
                row["supplier_name"],
                f"Risk: {row['composite_supplier_risk']:.2f}",
                f"Delay Rate: {row['delay_rate']:.1%} | Products: {int(row['num_products'])}",
                "#EF4444" if row["composite_supplier_risk"] > 0.35 else "#F59E0B"
            )
            
    with col2:
        st.subheader("Supplier Operational Metrics")
        render_data_table(sup_feat[["supplier_id", "supplier_name", "lead_time", "reliability_score", "delay_rate", "num_products", "composite_supplier_risk"]])
        
    st.markdown("---")
    st.subheader("Supplier Deep Dive")
    selected_sup = st.selectbox("Select Supplier ID to inspect:", sup_feat["supplier_id"].tolist())
    if selected_sup:
        s_row = sup_feat[sup_feat["supplier_id"] == selected_sup].iloc[0]
        render_insight_box("Supplier Analytical Insight", generate_supplier_risk_insight(s_row, int(s_row["num_products"]) * 12), "🏭")
