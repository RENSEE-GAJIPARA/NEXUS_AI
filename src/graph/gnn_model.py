"""Offline PyTorch Graph Neural Network (GNN / GraphSAGE) Experimentation Module for NEXUS AI."""
import torch
import torch.nn as nn
import torch.nn.functional as F
import networkx as nx
import numpy as np
import pandas as pd
from typing import Dict, Any

class GraphSAGENodeClassifier(nn.Module):
    """Simple 2-layer GraphSAGE Aggregator for node risk classification."""
    def __init__(self, in_channels: int, hidden_channels: int, out_channels: int):
        super().__init__()
        self.fc_self = nn.Linear(in_channels, hidden_channels)
        self.fc_neigh = nn.Linear(in_channels, hidden_channels)
        self.fc_out = nn.Linear(hidden_channels, out_channels)

    def forward(self, x: torch.Tensor, adj_norm: torch.Tensor) -> torch.Tensor:
        # Aggregation from neighbors
        neigh_agg = torch.matmul(adj_norm, x)
        h = F.relu(self.fc_self(x) + self.fc_neigh(neigh_agg))
        out = self.fc_out(h)
        return out

def run_gnn_experiment(G: nx.Graph, epochs: int = 20) -> Dict[str, Any]:
    """Train PyTorch GraphSAGE node risk classifier on the business graph."""
    if G.number_of_nodes() < 5:
        return {"status": "FAILED", "reason": "Graph too small"}
        
    nodes = list(G.nodes())
    num_nodes = len(nodes)
    
    # Simple node feature matrix: degree, centrality, node_type_one_hot
    adj = nx.to_numpy_array(G, nodelist=nodes)
    deg = adj.sum(axis=1, keepdims=True)
    
    # Normalized adjacency for GNN message passing
    deg_inv_sqrt = np.power(deg, -0.5, where=deg > 0)
    deg_inv_sqrt[deg == 0] = 0.0
    adj_norm = deg_inv_sqrt * adj * deg_inv_sqrt.T
    
    # Dummy node target labels (e.g. High Risk node = 1 if degree > 5)
    labels = (deg.squeeze() > 5).astype(int)
    
    X_tensor = torch.tensor(deg, dtype=torch.float32)
    adj_tensor = torch.tensor(adj_norm, dtype=torch.float32)
    y_tensor = torch.tensor(labels, dtype=torch.long)
    
    model = GraphSAGENodeClassifier(in_channels=1, hidden_channels=8, out_channels=2)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    criterion = nn.CrossEntropyLoss()
    
    losses = []
    model.train()
    for epoch in range(epochs):
        optimizer.zero_grad()
        out = model(X_tensor, adj_tensor)
        loss = criterion(out, y_tensor)
        loss.backward()
        optimizer.step()
        losses.append(round(float(loss.item()), 4))
        
    preds = out.argmax(dim=1).detach().numpy()
    acc = float((preds == labels).mean())
    
    return {
        "status": "SUCCESS",
        "algorithm": "PyTorch GraphSAGE Node Classifier",
        "num_nodes": num_nodes,
        "epochs": epochs,
        "final_loss": losses[-1],
        "training_accuracy": round(acc, 4),
        "loss_history": losses
    }
