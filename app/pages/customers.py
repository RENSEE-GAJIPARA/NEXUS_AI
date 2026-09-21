"""Customer Intelligence Page for NEXUS AI."""
import streamlit as st
import pandas as pd
from app.utils.data_loader import get_all_canonical_data
from app.components.cards import render_kpi_card
from app.components.charts import plot_donut_chart
from app.components.tables import render_data_table
from app.components.insights import render_insight_box
from src.models.risk import predict_customer_risk
from src.utils.insights import generate_customer_risk_insight

def render():
    st.header("Customer Intelligence & Risk Scoring")
    st.markdown("Predictive churn risk analytics, RFM customer segmentation, and profile deep-dives.")
    
    tables = get_all_canonical_data()
    df_cust = tables.get("customers", pd.DataFrame())
    df_tx = tables.get("transactions", pd.DataFrame())
    df_items = tables.get("transaction_items", pd.DataFrame())
    
    if df_cust.empty:
        st.warning("Customer data unavailable.")
        return
        
    risk_df = predict_customer_risk(df_cust, df_tx, df_items)
    
    # Safely merge risk and RFM features into customer dataset
    merge_cols = [c for c in risk_df.columns if c not in df_cust.columns or c == "customer_id"]
    merged_cust = df_cust.merge(risk_df[merge_cols], on="customer_id", how="left")
    
    # Risk Distribution Donut Chart
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Churn Risk Distribution")
        if "risk_band" in merged_cust.columns:
            counts = merged_cust["risk_band"].value_counts()
            fig_donut = plot_donut_chart(counts.index.tolist(), counts.values.tolist(), "Customer Risk Breakdown")
            st.plotly_chart(fig_donut, use_container_width=True)
        else:
            st.info("Risk distribution data unavailable.")
        
    with col2:
        st.subheader("At-Risk Customer Watchlist")
        if "risk_band" in merged_cust.columns:
            high_risk = merged_cust[merged_cust["risk_band"] == "High"].sort_values(by="risk_probability", ascending=False)
        else:
            high_risk = merged_cust
            
        desired_watchlist_cols = ["customer_id", "customer_segment", "recency_days", "frequency", "monetary_total", "risk_probability", "risk_band"]
        available_watchlist_cols = [col for col in desired_watchlist_cols if col in high_risk.columns]
        render_data_table(high_risk[available_watchlist_cols].head(10))
        
    st.markdown("---")
    st.subheader("Customer Deep Dive")
    selected_cid = st.selectbox("Select Customer ID to inspect:", merged_cust["customer_id"].tolist())
    
    if selected_cid:
        c_row = merged_cust[merged_cust["customer_id"] == selected_cid].iloc[0]
        c1, c2, c3 = st.columns(3)
        
        prob = float(c_row.get("risk_probability", 0.0))
        band = str(c_row.get("risk_band", "Low"))
        rec = float(c_row.get("recency_days", 0.0))
        seg = str(c_row.get("customer_segment", "Standard"))
        monetary = float(c_row.get("monetary_total", 0.0))
        freq = float(c_row.get("frequency", 0.0))
        
        with c1:
            render_kpi_card("Risk Score", f"{prob:.1%}", f"Band: {band}", "#DC2626" if band == "High" else "#16A34A")
        with c2:
            render_kpi_card("Inactivity Recency", f"{int(rec)} Days", f"Segment: {seg}")
        with c3:
            render_kpi_card("Lifetime Spend", f"${monetary:,.2f}", f"Orders: {int(freq)}")
            
        render_insight_box("Customer Intelligence Summary", generate_customer_risk_insight(c_row))

