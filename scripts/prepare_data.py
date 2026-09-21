"""Data Preparation Pipeline for NEXUS AI."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.data.ingestion import load_canonical_data
from src.data.cleaning import clean_canonical_tables
from src.data.validation import validate_datasets
from src.utils.paths import DATA_PROCESSED_DIR
from src.utils.logging import logger

def main():
    logger.info("Running Data Preparation Pipeline...")
    tables = load_canonical_data()
    cleaned_tables = clean_canonical_tables(tables)
    
    # Save cleaned tables
    for name, df in cleaned_tables.items():
        df.to_csv(DATA_PROCESSED_DIR / f"{name}.csv", index=False)
        try:
            df.to_parquet(DATA_PROCESSED_DIR / f"{name}.parquet", index=False)
        except Exception:
            pass
        
    validation = validate_datasets(cleaned_tables)
    logger.info(f"Data Quality Score: {validation['quality_score']}% ({validation['passed_checks']}/{validation['total_checks']} checks passed)")
    logger.info("Data preparation complete.")

if __name__ == "__main__":
    main()
