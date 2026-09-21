"""Unit tests for ML models and Anomaly Detection in NEXUS AI."""
import unittest
from src.data.ingestion import load_canonical_data
from src.models.risk import predict_customer_risk
from src.anomaly.isolation_forest import detect_transaction_anomalies

class TestModelsAndAnomalies(unittest.TestCase):
    def test_predict_customer_risk(self):
        tables = load_canonical_data()
        preds = predict_customer_risk(tables["customers"], tables["transactions"], tables["transaction_items"])
        self.assertIn("risk_probability", preds.columns)
        self.assertIn("risk_band", preds.columns)
        self.assertEqual(len(preds), len(tables["customers"]))

    def test_detect_anomalies(self):
        tables = load_canonical_data()
        anom = detect_transaction_anomalies(tables["transactions"], tables["transaction_items"])
        self.assertIn("anomaly_score", anom.columns)
        self.assertIn("is_anomaly", anom.columns)
        self.assertEqual(len(anom), len(tables["transactions"]))

if __name__ == "__main__":
    unittest.main()
