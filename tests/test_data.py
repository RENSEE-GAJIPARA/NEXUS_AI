"""Unit tests for Data Engineering & Validation in NEXUS AI."""
import unittest
from src.data.ingestion import load_canonical_data
from src.data.validation import validate_datasets

class TestDataEngineering(unittest.TestCase):
    def test_load_canonical_data(self):
        tables = load_canonical_data()
        self.assertIn("customers", tables)
        self.assertIn("transactions", tables)
        self.assertFalse(tables["customers"].empty)
        self.assertEqual(len(tables["customers"]), 500)

    def test_validate_datasets(self):
        tables = load_canonical_data()
        report = validate_datasets(tables)
        self.assertGreaterEqual(report["quality_score"], 90.0)
        self.assertGreater(report["passed_checks"], 0)

if __name__ == "__main__":
    unittest.main()
