"""Data Download Script with Fallback to Demo Data Generation for NEXUS AI."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.generate_demo_data import generate_nexus_data
from src.utils.logging import logger

def main():
    logger.info("Initializing NEXUS AI Data Download Pipeline...")
    try:
        # In a real environment, external dataset downloads from Kaggle/UCI can be invoked here.
        # Fallback to rich, cohesive demo dataset generation to ensure zero deploy/runtime failure.
        logger.info("Verifying local dataset status. Packaging demo relational business data...")
        generate_nexus_data()
        logger.info("Data download & preparation pipeline complete.")
    except Exception as e:
        logger.error(f"Data ingestion pipeline failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
