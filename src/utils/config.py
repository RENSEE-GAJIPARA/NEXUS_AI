"""Configuration management for NEXUS AI."""
import os
from dataclasses import dataclass

@dataclass
class NexusConfig:
    ENV: str = os.getenv("NEXUS_ENV", "production")
    LOG_LEVEL: str = os.getenv("NEXUS_LOG_LEVEL", "INFO")
    DEMO_MODE: bool = os.getenv("DEMO_MODE", "true").lower() == "true"
    
    # Model Thresholds
    CHURN_INACTIVITY_DAYS: int = 60
    ANOMALY_CONTAMINATION: float = 0.05
    HIGH_RISK_THRESHOLD: float = 0.70
    MEDIUM_RISK_THRESHOLD: float = 0.40
    
    # Forecast Settings
    DEFAULT_FORECAST_HORIZON: int = 14
    MAX_FORECAST_HORIZON: int = 30

config = NexusConfig()
