"""Scenario Lab Page for NEXUS AI."""
import streamlit as st
import pandas as pd
from app.utils.data_loader import get_all_canonical_data
from app.components.cards import render_kpi_card
from app.components.insights import render_methodology_disclaimer
from src.scenarios.scenario_engine import run_what_if_simulation

def render():
    st.header("Scenario Lab — Interactive What-If Simulation")
    st.markdown("Simulate revenue and demand projections by adjusting pricing elasticity, promotional discounts, and supply chain constraints.")
    
    tables = get_all_canonical_data()
    df_tx = tables.get("transactions", pd.DataFrame())
    
    if df_tx.empty:
        base_rev = 100000.0
        base_dem = 5000.0
    else:
        base_rev = float(df_tx["total_amount"].sum())
        base_dem = float(len(df_tx))
        
    st.sidebar.markdown("### Scenario Controls")
    price_pct = st.sidebar.slider("Unit Price Adjustment (%)", -30.0, 30.0, 0.0, step=1.0)
    disc_pct = st.sidebar.slider("Discount Rate Change (%)", -15.0, 25.0, 0.0, step=1.0)
    inv_factor = st.sidebar.slider("Inventory Level Multiplier", 0.5, 2.0, 1.0, step=0.1)
    sup_avail = st.sidebar.slider("Supplier Availability Cap (%)", 20.0, 100.0, 100.0, step=5.0)
    
    res = run_what_if_simulation(
        base_revenue=base_rev,
        base_demand=base_dem,
        price_change_pct=price_pct,
        discount_change_pct=disc_pct,
        inventory_factor=inv_factor,
        supplier_availability_pct=sup_avail
    )
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("Baseline Revenue", f"${res['baseline_revenue']:,.2f}", "365-Day Historical Baseline")
    with col2:
        render_kpi_card("Simulated Revenue", f"${res['simulated_revenue']:,.2f}", f"Delta: {res['revenue_pct_diff']:+.2f}%", "#16A34A" if res['revenue_pct_diff'] >= 0 else "#DC2626")
    with col3:
        render_kpi_card("Baseline Demand", f"{res['baseline_demand']:,.0f}", "Transactions / Units")
    with col4:
        render_kpi_card("Simulated Demand", f"{res['simulated_demand']:,.0f}", f"Delta: {res['demand_pct_diff']:+.2f}%", "#2563EB")
        
    st.markdown("---")
    st.subheader("Simulation Analysis Summary")
    
    st.write(
        f"Under the selected parameters (**Price:** {price_pct:+.1f}%, **Discount:** {disc_pct:+.1f}%, **Inventory Factor:** {inv_factor:.1f}x, **Supplier Availability:** {sup_avail:.0f}%), "
        f"projected annual revenue shifts by **${res['revenue_abs_diff']:+,.2f}** ({res['revenue_pct_diff']:+.2f}%). "
        f"Simulated transaction volume changes by **{res['demand_abs_diff']:+,.0f}** units."
    )
    
    st.markdown("---")
    render_methodology_disclaimer(res["disclaimer"])

