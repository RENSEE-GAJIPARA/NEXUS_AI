"""Interactive NetworkX / Plotly Graph Visualizer for NEXUS AI."""
import plotly.graph_objects as go
import networkx as nx
from src.graph.graph_analysis import extract_subgraph

NODE_COLORS = {
    "Customer": "#2563EB",
    "Product": "#16A34A",
    "Supplier": "#DC2626",
    "Store": "#D97706",
    "Location": "#9333EA",
    "Transaction": "#64748B"
}

def render_plotly_graph(G: nx.Graph, center_node: str = None, radius: int = 1, max_nodes: int = 40) -> go.Figure:
    """Render interactive network graph in Plotly."""
    if G is None or G.number_of_nodes() == 0:
        fig = go.Figure()
        fig.update_layout(title="No graph data available")
        return fig
        
    if center_node and center_node in G:
        sub_g = extract_subgraph(G, center_node=center_node, radius=radius, max_nodes=max_nodes)
    else:
        # Sample top degree nodes for optimal browser performance
        top_nodes = sorted(G.nodes(), key=lambda n: G.degree(n), reverse=True)[:max_nodes]
        sub_g = G.subgraph(top_nodes).copy()
        
    pos = nx.spring_layout(sub_g, seed=42, k=0.35)
    
    # Edges
    edge_x = []
    edge_y = []
    for edge in sub_g.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color="#94A3B8"),
        hoverinfo="none",
        mode="lines"
    )
    
    # Nodes
    node_x = []
    node_y = []
    node_color = []
    node_text = []
    node_size = []
    
    for node in sub_g.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        
        ntype = sub_g.nodes[node].get("node_type", "Unknown")
        name = sub_g.nodes[node].get("name", node)
        deg = sub_g.degree(node)
        
        node_color.append(NODE_COLORS.get(ntype, "#64748B"))
        node_text.append(f"Node: {node}<br>Name: {name}<br>Type: {ntype}<br>Degree: {deg}")
        node_size.append(max(12, min(30, 8 + deg * 2)))
        
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode="markers+text",
        hoverinfo="text",
        text=[node for node in sub_g.nodes()],
        textposition="top center",
        textfont=dict(color="#172033", size=9),
        hovertext=node_text,
        marker=dict(
            color=node_color,
            size=node_size,
            line=dict(width=1.5, color="#FFFFFF")
        )
    )
    
    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        title=f"Business Relationship Graph ({sub_g.number_of_nodes()} Nodes, {sub_g.number_of_edges()} Edges)",
        showlegend=False,
        hovermode="closest",
        margin=dict(b=20, l=20, r=20, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFFFF",
        font=dict(color="#172033", family="Inter, sans-serif")
    )
    return fig

