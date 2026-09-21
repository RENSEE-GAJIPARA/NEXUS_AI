"""Unit tests for Graph Intelligence in NEXUS AI."""
import unittest
from src.data.ingestion import load_canonical_data
from src.graph.graph_builder import build_business_graph
from src.graph.graph_analysis import analyze_graph

class TestGraphIntelligence(unittest.TestCase):
    def test_build_business_graph(self):
        tables = load_canonical_data()
        G = build_business_graph(tables)
        self.assertGreater(G.number_of_nodes(), 0)
        self.assertGreater(G.number_of_edges(), 0)
        
        metrics = analyze_graph(G)
        self.assertEqual(metrics["num_nodes"], G.number_of_nodes())

if __name__ == "__main__":
    unittest.main()
