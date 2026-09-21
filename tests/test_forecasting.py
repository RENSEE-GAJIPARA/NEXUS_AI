"""Unit tests for Forecasting & Scenario Engine in NEXUS AI."""
import unittest
from src.data.ingestion import load_canonical_data
from src.forecasting.models import generate_multi_step_forecast
from src.scenarios.scenario_engine import run_what_if_simulation

class TestForecastingAndScenarios(unittest.TestCase):
    def test_forecasting(self):
        tables = load_canonical_data()
        fc = generate_multi_step_forecast(tables["transactions"], horizon_days=7)
        self.assertEqual(len(fc), 7)
        self.assertIn("forecasted_revenue", fc.columns)

    def test_scenario_simulation(self):
        res = run_what_if_simulation(base_revenue=100000.0, base_demand=1000.0, price_change_pct=10.0)
        self.assertEqual(res["baseline_revenue"], 100000.0)
        self.assertIn("simulated_revenue", res)
        self.assertIn("disclaimer", res)

if __name__ == "__main__":
    unittest.main()
