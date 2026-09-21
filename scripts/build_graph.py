"""Offline Graph Builder & GNN Experimentation Script for NEXUS AI."""
import sys
import joblib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.data.ingestion import load_canonical_data
from src.graph.graph_builder import build_business_graph
from src.graph.graph_analysis import analyze_graph
from src.graph.graph_embeddings import generate_graph_embeddings
from src.graph.gnn_model import run_gnn_experiment
from src.utils.paths import MODELS_DIR
from src.utils.logging import logger

def main():
    logger.info("Building NEXUS AI Business Relationship Graph...")
    tables = load_canonical_data()
    
    G = build_business_graph(tables)
    metrics = analyze_graph(G)
    logger.info(f"Graph Metrics: {metrics['num_nodes']} Nodes, {metrics['num_edges']} Edges, Density: {metrics['graph_density']}")
    
    # Generate low-dimensional embeddings
    logger.info("Generating Graph Node Embeddings...")
    df_emb = generate_graph_embeddings(G)
    
    # Run PyTorch GNN Experiment
    logger.info("Executing PyTorch GraphSAGE Node Classifier Experiment...")
    gnn_res = run_gnn_experiment(G)
    logger.info(f"GNN Result: Status={gnn_res['status']}, Loss={gnn_res.get('final_loss')}, Accuracy={gnn_res.get('training_accuracy')}")
    
    # Save graph artifact
    joblib.dump(G, MODELS_DIR / "business_graph.joblib")
    df_emb.to_csv(MODELS_DIR / "graph_embeddings.csv", index=False)
    logger.info("Graph artifacts saved to models/.")

if __name__ == "__main__":
    main()
