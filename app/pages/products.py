"""Product Intelligence Page for NEXUS AI."""
import streamlit as st
import pandas as pd
from app.utils.data_loader import get_all_canonical_data
from app.components.cards import render_kpi_card
from app.components.charts import plot_bar_chart
from app.components.tables import render_data_table
from src.features.product_features import build_product_features

def render():
    st.header("Product Intelligence & Performance")
    st.markdown("Sales velocity, revenue contribution, margin dynamics, and inventory stockout signals.")
    
    tables = get_all_canonical_data()
    df_prod = tables.get("products", pd.DataFrame())
    df_tx = tables.get("transactions", pd.DataFrame())
    df_items = tables.get("transaction_items", pd.DataFrame())
    df_inv = tables.get("inventory", pd.DataFrame())
    
    if df_prod.empty:
        st.warning("Product data unavailable.")
        return
        
    prod_feat = build_product_features(df_prod, df_items, df_tx)
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Top Revenue Products")
        top_rev = prod_feat.sort_values(by="total_revenue", ascending=False).head(10)
        fig_bar = plot_bar_chart(top_rev, "product_id", "total_revenue", "Top 10 Products by Revenue ($)")
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with c2:
        st.subheader("Category Revenue Breakdown")
        cat_agg = prod_feat.groupby("category")["total_revenue"].sum().reset_index()
        fig_cat = plot_bar_chart(cat_agg, "category", "total_revenue", "Revenue by Category ($)")
        st.plotly_chart(fig_cat, use_container_width=True)
        
    st.markdown("---")
    st.subheader("Inventory Stockout Risk Watchlist")
    if not df_inv.empty and "stockout_risk" in df_inv.columns:
        low_stock = df_inv[df_inv["stockout_risk"] == 1].merge(df_prod[["product_id", "product_name", "category", "supplier_id"]], on="product_id", how="left")
        desired_low = ["product_id", "product_name", "category", "store_id", "stock_level", "reorder_point", "supplier_id"]
        avail_low = [c for c in desired_low if c in low_stock.columns]
        render_data_table(low_stock[avail_low].head(10))
    else:
        desired_prod = ["product_id", "product_name", "category", "unit_price", "total_units_sold", "total_revenue"]
        avail_prod = [c for c in desired_prod if c in prod_feat.columns]
        render_data_table(prod_feat[avail_prod].head(10))

