"""Automated Data Validation and Data Quality Scoring for NEXUS AI."""
import pandas as pd
import numpy as np
from typing import Dict, Any

def validate_datasets(tables: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    """Perform multi-table integrity and schema validation checks.
    Returns calculated quality score and metrics breakdown.
    """
    total_checks = 0
    passed_checks = 0
    issues = []
    table_metrics = {}

    for name, df in tables.items():
        if df.empty:
            issues.append(f"Table '{name}' is empty.")
            continue
            
        n_rows = len(df)
        null_count = df.isnull().sum().sum()
        dup_count = df.duplicated().sum()
        
        # Check 1: Completeness
        completeness_rate = 1.0 - (null_count / (n_rows * len(df.columns))) if n_rows > 0 else 0.0
        total_checks += 1
        if completeness_rate >= 0.95:
            passed_checks += 1
        else:
            issues.append(f"Table '{name}' has low completeness ({completeness_rate:.1%}).")
            
        # Check 2: Uniqueness (no duplicate rows)
        uniqueness_rate = 1.0 - (dup_count / n_rows) if n_rows > 0 else 0.0
        total_checks += 1
        if uniqueness_rate >= 0.99:
            passed_checks += 1
        else:
            issues.append(f"Table '{name}' contains {dup_count} duplicate rows.")

        # Check 3: Domain Rules
        domain_valid = True
        if name == "transactions" and "total_amount" in df.columns:
            neg_amt = (df["total_amount"] < 0).sum()
            if neg_amt > 0:
                domain_valid = False
                issues.append(f"Found {neg_amt} transactions with negative amount.")
        elif name == "transaction_items" and "quantity" in df.columns:
            neg_qty = (df["quantity"] <= 0).sum()
            if neg_qty > 0:
                domain_valid = False
                issues.append(f"Found {neg_qty} transaction items with invalid quantity <= 0.")
        elif name == "products" and "unit_price" in df.columns:
            invalid_p = (df["unit_price"] <= 0).sum()
            if invalid_p > 0:
                domain_valid = False
                issues.append(f"Found {invalid_p} products with zero or negative price.")
                
        total_checks += 1
        if domain_valid:
            passed_checks += 1

        table_metrics[name] = {
            "row_count": n_rows,
            "col_count": len(df.columns),
            "null_count": int(null_count),
            "dup_count": int(dup_count),
            "completeness_score": round(float(completeness_rate * 100), 2),
            "uniqueness_score": round(float(uniqueness_rate * 100), 2),
        }

    # Check 4: Referential Integrity
    ref_checks_passed = 0
    ref_checks_total = 0
    if "transactions" in tables and "customers" in tables:
        ref_checks_total += 1
        tx_cust = set(tables["transactions"]["customer_id"].unique())
        all_cust = set(tables["customers"]["customer_id"].unique())
        orphan_cust = tx_cust - all_cust
        if not orphan_cust:
            ref_checks_passed += 1
        else:
            issues.append(f"Found {len(orphan_cust)} transactions referencing non-existent customer IDs.")

    if "transactions" in tables and "stores" in tables:
        ref_checks_total += 1
        tx_str = set(tables["transactions"]["store_id"].unique())
        all_str = set(tables["stores"]["store_id"].unique())
        orphan_str = tx_str - all_str
        if not orphan_str:
            ref_checks_passed += 1
        else:
            issues.append(f"Found {len(orphan_str)} transactions referencing non-existent store IDs.")
            
    total_checks += ref_checks_total
    passed_checks += ref_checks_passed

    overall_quality_score = round(float((passed_checks / total_checks) * 100), 1) if total_checks > 0 else 100.0

    return {
        "quality_score": overall_quality_score,
        "total_checks": total_checks,
        "passed_checks": passed_checks,
        "table_metrics": table_metrics,
        "issues": issues
    }
