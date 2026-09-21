"""Graph Intelligence Page for NEXUS AI."""
import streamlit as st
import pandas as pd
from app.utils.model_loader import get_business_graph
from app.components.graph_view import render_plotly_graph
from app.components.tables import render_data_table
from app.components.insights import render_insight_box
from src.graph.graph_analysis import analyze_graph

def render():
    st.header("Graph Intelligence & Entity Topology")
    st.markdown("Heterogeneous relationship graphs mapping Customer → Store → Product → Supplier dependencies.")
    
    G = get_business_graph()
    if G is None:
        st.warning("Business Graph object not found.")
        return
        
    metrics = analyze_graph(G)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Graph Nodes", metrics.get("num_nodes", 0))
    with c2:
        st.metric("Total Relationships (Edges)", metrics.get("num_edges", 0))
    with c3:
        st.metric("Graph Density", metrics.get("graph_density", 0.0))
    with c4:
        st.metric("Connected Subgraphs", metrics.get("num_connected_components", 1))
        
    st.markdown("---")
    
    # Subgraph Exploration Controls
    col_ctrl, col_graph = st.columns([1, 2])
    with col_ctrl:
        st.subheader("Sub-Graph Filter")
        all_nodes = list(G.nodes())
        selected_node = st.selectbox("Center Entity Node:", ["(Global Top Nodes)"] + all_nodes)
        radius = st.slider("Hop Radius (Ego Graph):", 1, 3, 1)
        max_n = st.slider("Max Display Nodes:", 10, 80, 35)
        
        node_query = None if selected_node == "(Global Top Nodes)" else selected_node
        
    with col_graph:
        fig_g = render_plotly_graph(G, center_node=node_query, radius=radius, max_nodes=max_n)
        st.plotly_chart(fig_g, use_container_width=True)
        
    st.markdown("---")
    st.subheader("Supplier Network Vulnerability Concentration")
    if "top_suppliers_exposure" in metrics and isinstance(metrics["top_suppliers_exposure"], pd.DataFrame):
        render_data_table(metrics["top_suppliers_exposure"].head(10))
