"""Offline Model Training Script for NEXUS AI."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.data.ingestion import load_canonical_data
from src.models.risk import train_customer_risk_model
from src.anomaly.isolation_forest import train_anomaly_model
from src.forecasting.models import train_forecasting_model
from src.utils.logging import logger

def train_all_models():
    logger.info("Loading processed canonical datasets...")
    tables = load_canonical_data()
    
    if "customers" not in tables or tables["customers"].empty:
        logger.error("No data found to train models.")
        return
        
    logger.info("1/3 Training Customer Churn Risk Models...")
    train_customer_risk_model(tables["customers"], tables["transactions"], tables["transaction_items"])
    
    logger.info("2/3 Training Isolation Forest Anomaly Detector...")
    train_anomaly_model(tables["transactions"], tables["transaction_items"])
    
    logger.info("3/3 Training Time-Series Demand Forecaster...")
    train_forecasting_model(tables["transactions"])
    
    logger.info("All NEXUS AI model artifacts successfully trained & persisted to models/.")

if __name__ == "__main__":
    train_all_models()
