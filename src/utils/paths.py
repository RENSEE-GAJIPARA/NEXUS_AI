"""Path resolution utilities for NEXUS AI.
Ensures reproducible cross-platform file paths.
"""
from pathlib import Path

# Base Root Directory of NEXUS-AI
ROOT_DIR = Path(__file__).resolve().parents[2]

# Subdirectories
APP_DIR = ROOT_DIR / "app"
SRC_DIR = ROOT_DIR / "src"
DATA_DIR = ROOT_DIR / "data"
DATA_RAW_DIR = DATA_DIR / "raw"
DATA_PROCESSED_DIR = DATA_DIR / "processed"
DATA_SYNTHETIC_DIR = DATA_DIR / "synthetic"
DATA_SAMPLE_DIR = DATA_DIR / "sample"
MODELS_DIR = ROOT_DIR / "models"
DOCS_DIR = ROOT_DIR / "docs"
LOGS_DIR = ROOT_DIR / "logs"

def get_processed_data_path(filename: str) -> Path:
    """Get path to a processed dataset file."""
    return DATA_PROCESSED_DIR / filename

def get_model_path(filename: str) -> Path:
    """Get path to a trained model artifact."""
    return MODELS_DIR / filename
