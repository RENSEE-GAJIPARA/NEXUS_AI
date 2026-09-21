"""About & Methodology Page for NEXUS AI."""
import streamlit as st
from app.components.insights import render_methodology_disclaimer

def render():
    st.header("About NEXUS AI — Architecture & Methodology")
    st.markdown("NEXUS AI is an autonomous graph-based business intelligence and decision-support engine.")
    
    st.markdown("""
    ### 🏛️ System Architecture Overview
    NEXUS AI connects heterogeneous business entities (**Customer**, **Product**, **Supplier**, **Store**, **Location**, **Transaction**) 
    into a unified graph network and predictive analytical pipeline.

    ```
    Data Ingestion -> Cleaning & Validation -> Feature Engineering
          │
          ├── Predictive ML (Gradient Boosting Churn Risk)
          ├── Anomaly Detection (Isolation Forest Multi-Variable Outliers)
          ├── Time-Series Forecasting (Gradient Boosting Lag-Feature Horizon)
          ├── Graph Intelligence (NetworkX Topology + PyTorch GraphSAGE GNN)
          └── Explainability & Scenarios (SHAP Feature Attribution + What-If Engine)
          │
          └── Unified Streamlit BI & Decision Support Application
    ```

    ---

    ### 🔬 Methodology Breakdown

    #### 1. Predictive Risk Engine
    - **Method:** Supervised classification (Gradient Boosting / Random Forest).
    - **Target:** Proxy customer churn (Inactivity > 60 days).
    - **Evaluation:** Evaluated chronologically via F1-Score, ROC-AUC, and Precision-Recall AUC.

    #### 2. Multi-Dimensional Anomaly Detection
    - **Method:** Isolation Forest unsupervised tree ensemble.
    - **Features:** Transaction total, item count, unit prices, discount rates.
    - **Explanation:** Deterministic distance metrics derived from feature standard deviations.

    #### 3. Temporal Demand Forecasting
    - **Method:** Recursive multi-step Gradient Boosting regressor.
    - **Validation:** Chronological split (no future data leakage). Lags (1, 7, 14, 30 days) + rolling stats.

    #### 4. Graph Intelligence & GNN
    - **Method:** NetworkX heterogeneous graph + Spectral SVD Node Embeddings.
    - **GNN:** 2-Layer PyTorch GraphSAGE node risk aggregator trained offline.

    #### 5. What-If Scenario Engine
    - **Method:** Mathematical price-elasticity of demand simulation engine.
    - **Parameters:** Elasticity factor (-1.2), discount elasticity, supply constraint caps.
    """)
    
    st.markdown("---")
    render_methodology_disclaimer()
