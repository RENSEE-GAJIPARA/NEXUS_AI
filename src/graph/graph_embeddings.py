"""Graph Node Embeddings Generator for NEXUS AI."""
import networkx as nx
import numpy as np
import pandas as pd
from scipy.sparse.linalg import svds

def generate_graph_embeddings(G: nx.Graph, embedding_dim: int = 16) -> pd.DataFrame:
    """Generate low-dimensional node embeddings using Spectral/SVD Decomposition on Adjacency Matrix."""
    if G.number_of_nodes() == 0:
        return pd.DataFrame()
        
    nodes = list(G.nodes())
    node_to_idx = {node: i for i, node in enumerate(nodes)}
    
    adj = nx.to_scipy_sparse_array(G, nodelist=nodes, weight="weight", format="csr", dtype=float)
    
    k = min(embedding_dim, G.number_of_nodes() - 1)
    if k < 2:
        return pd.DataFrame({"node_id": nodes})
        
    u, s, vt = svds(adj, k=k)
    embeddings = u * np.sqrt(s)
    
    df_emb = pd.DataFrame(embeddings, columns=[f"emb_{i}" for i in range(k)])
    df_emb.insert(0, "node_id", nodes)
    df_emb.insert(1, "node_type", [G.nodes[n].get("node_type", "Unknown") for n in nodes])
    
    return df_emb
