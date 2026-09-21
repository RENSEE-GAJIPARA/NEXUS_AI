"""Model Center Page for NEXUS AI."""
import streamlit as st
import pandas as pd
from app.utils.model_loader import get_model_and_metadata
from app.components.cards import render_kpi_card
from app.components.charts import plot_bar_chart
from app.components.tables import render_data_table
from src.explainability.shap_explainer import calculate_feature_importance

def render():
    st.header("Model Center — Machine Learning Registry")
    st.markdown("Model metadata tracking, cross-algorithm validation benchmarks, and feature importance explainability.")
    
    models = ["customer_risk_model", "anomaly_model", "demand_forecast_model"]
    selected_model_name = st.selectbox("Select Model Artifact to Inspect:", models)
    
    model_obj, metadata = get_model_and_metadata(selected_model_name)
    
    if not metadata:
        st.warning("Model metadata unavailable.")
        return
        
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi_card("Algorithm", metadata.get("algorithm", "Unknown"), "Model Class")
    with c2:
        render_kpi_card("Target Variable", metadata.get("target", "N/A"), "Objective")
    with c3:
        render_kpi_card("Feature Count", len(metadata.get("features", [])), "Inputs")
    with c4:
        render_kpi_card("Training Rows", f"{metadata.get('dataset_rows', 0):,}", "Samples")
        
    st.markdown("---")
    st.subheader("Feature Importance Attribution")
    feat_names = metadata.get("features", [])
    if model_obj and feat_names:
        df_imp = calculate_feature_importance(model_obj, feat_names)
        if not df_imp.empty:
            fig_imp = plot_bar_chart(df_imp, "importance", "feature", "Feature Relative Weight", orientation="h")
            st.plotly_chart(fig_imp, use_container_width=True)
            
    st.markdown("---")
    st.subheader("Full Model Metadata JSON")
    st.json(metadata)
