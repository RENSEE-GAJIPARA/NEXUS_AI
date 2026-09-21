"""Forecast Center Page for NEXUS AI."""
import streamlit as st
import pandas as pd
from app.utils.data_loader import get_all_canonical_data
from app.utils.model_loader import get_model_and_metadata
from app.components.cards import render_kpi_card
from app.components.charts import plot_forecast_chart
from app.components.tables import render_data_table
from src.features.time_features import build_daily_time_series_features
from src.forecasting.models import generate_multi_step_forecast

def render():
    st.header("Forecast Center — Temporal Demand & Revenue")
    st.markdown("Multi-step recursive Gradient Boosting time-series forecasting with chronological split validation.")
    
    tables = get_all_canonical_data()
    df_tx = tables.get("transactions", pd.DataFrame())
    
    if df_tx.empty:
        st.warning("Transaction history unavailable.")
        return
        
    daily = build_daily_time_series_features(df_tx)
    daily_chart = daily.rename(columns={"transaction_date": "date", "daily_revenue": "revenue"}).tail(90)
    
    horizon = st.radio("Forecast Horizon:", [7, 14, 30], index=1, horizontal=True)
    
    forecast_df = generate_multi_step_forecast(df_tx, horizon_days=horizon)
    
    _, metadata = get_model_and_metadata("demand_forecast_model")
    metrics = metadata.get("metrics", {})
    
    col1, col2, col3 = st.columns(3)
    with col1:
        render_kpi_card("Projected Horizon Revenue", f"${forecast_df['forecasted_revenue'].sum():,.2f}", f"Next {horizon} Days Total", "#10B981")
    with col2:
        render_kpi_card("Model MAE", f"${metrics.get('mae', 0.0):,.2f}", "Gradient Boosting Error", "#3B82F6")
    with col3:
        render_kpi_card("Model SMAPE", f"{metrics.get('smape', 0.0):.2f}%", "Symmetric MAPE", "#8B5CF6")
        
    st.markdown("---")
    st.subheader("Historical Sales vs Forward Forecast")
    fig_fc = plot_forecast_chart(daily_chart, forecast_df, f"{horizon}-Day Revenue Projection ($)")
    st.plotly_chart(fig_fc, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Daily Forecast Table")
    render_data_table(forecast_df)
