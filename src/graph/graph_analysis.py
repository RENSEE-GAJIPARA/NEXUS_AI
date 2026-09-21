"""Graph Analytics & Vulnerability Metrics for NEXUS AI."""
import networkx as nx
import pandas as pd
from typing import Dict, Any

def analyze_graph(G: nx.Graph) -> Dict[str, Any]:
    """Calculate key graph network metrics."""
    if G.number_of_nodes() == 0:
        return {}
        
    degree_dict = dict(G.degree())
    degree_centrality = nx.degree_centrality(G)
    
    # Calculate degree distribution by node type
    node_types = {}
    for n, data in G.nodes(data=True):
        ntype = data.get("node_type", "Unknown")
        node_types[ntype] = node_types.get(ntype, 0) + 1
        
    num_components = nx.number_connected_components(G)
    
    # Calculate Supplier Dependency Vulnerability Score
    supplier_exposure = []
    for n, data in G.nodes(data=True):
        if data.get("node_type") == "Supplier":
            prod_neighbors = [neighbor for neighbor in G.neighbors(n) if G.nodes[neighbor].get("node_type") == "Product"]
            cust_neighbors = set()
            for p in prod_neighbors:
                cust_neighbors.update([c for c in G.neighbors(p) if G.nodes[c].get("node_type") == "Customer"])
                
            supplier_exposure.append({
                "supplier_id": n,
                "supplier_name": data.get("name", n),
                "products_count": len(prod_neighbors),
                "connected_customers": len(cust_neighbors),
                "degree": degree_dict.get(n, 0),
                "centrality": round(float(degree_centrality.get(n, 0.0)), 4)
            })
            
    df_sup_exposure = pd.DataFrame(supplier_exposure).sort_values(by="connected_customers", ascending=False)
    
    return {
        "num_nodes": G.number_of_nodes(),
        "num_edges": G.number_of_edges(),
        "node_type_counts": node_types,
        "num_connected_components": num_components,
        "graph_density": round(float(nx.density(G)), 5),
        "top_suppliers_exposure": df_sup_exposure
    }

def extract_subgraph(G: nx.Graph, center_node: str, radius: int = 2, max_nodes: int = 50) -> nx.Graph:
    """Extract ego subgraph around a center node for browser UI performance."""
    if center_node not in G:
        return nx.Graph()
        
    ego = nx.ego_graph(G, center_node, radius=radius)
    if ego.number_of_nodes() > max_nodes:
        # Sample top degree nodes
        top_nodes = sorted(ego.nodes(), key=lambda n: ego.degree(n), reverse=True)[:max_nodes]
        if center_node not in top_nodes:
            top_nodes.append(center_node)
        ego = ego.subgraph(top_nodes).copy()
        
    return ego
