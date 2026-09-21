"""Unit tests for Feature Engineering in NEXUS AI."""
import unittest
from src.data.ingestion import load_canonical_data
from src.features.customer_features import build_customer_features
from src.features.supplier_features import build_supplier_features

class TestFeatureEngineering(unittest.TestCase):
    def test_customer_features(self):
        tables = load_canonical_data()
        df_feat = build_customer_features(tables["customers"], tables["transactions"], tables["transaction_items"])
        self.assertIn("recency_days", df_feat.columns)
        self.assertIn("proxy_churn", df_feat.columns)
        self.assertEqual(len(df_feat), len(tables["customers"]))

    def test_supplier_features(self):
        tables = load_canonical_data()
        df_sup = build_supplier_features(tables["suppliers"], tables["products"], tables["transaction_items"])
        self.assertIn("composite_supplier_risk", df_sup.columns)
        self.assertEqual(len(df_sup), len(tables["suppliers"]))

if __name__ == "__main__":
    unittest.main()
