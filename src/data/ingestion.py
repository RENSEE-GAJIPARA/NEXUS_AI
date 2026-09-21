"""Data Ingestion pipeline for NEXUS AI."""
import os
from pathlib import Path
import pandas as pd
from typing import Dict, Optional
from src.utils.paths import DATA_PROCESSED_DIR
from src.utils.logging import logger

def load_canonical_data(data_dir: Optional[Path] = None) -> Dict[str, pd.DataFrame]:
    """Load all canonical business tables from parquet or csv."""
    target_dir = data_dir or DATA_PROCESSED_DIR
    tables = [
        "locations", "suppliers", "stores", "products",
        "customers", "calendar", "transactions", "transaction_items", "inventory"
    ]
    data = {}
    for table in tables:
        pq_file = target_dir / f"{table}.parquet"
        csv_file = target_dir / f"{table}.csv"
        
        if csv_file.exists():
            data[table] = pd.read_csv(csv_file)
        elif pq_file.exists():
            try:
                data[table] = pd.read_parquet(pq_file)
            except Exception:
                logger.warning(f"Could not read parquet for '{table}'.")
                data[table] = pd.DataFrame()
        else:
            logger.warning(f"Table '{table}' not found in {target_dir}")
            data[table] = pd.DataFrame()
            
    return data
