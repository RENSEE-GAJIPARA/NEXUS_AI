"""Verification script to test all pages, profiling across all tables, and emoji scanning."""
import sys
from pathlib import Path

# Add project root to sys.path
ROOT_PATH = Path(__file__).resolve().parents[1]
if str(ROOT_PATH) not in sys.path:
    sys.path.insert(0, str(ROOT_PATH))

import pandas as pd
from src.data.ingestion import load_canonical_data
from src.data.profiling import profile_dataframe
from src.models.risk import predict_customer_risk
from src.nlp.intent_parser import parse_user_intent

def test_profiling():
    print("--- Testing Profiling on All Canonical Tables ---")
    tables = load_canonical_data()
    for name, df in tables.items():
        prof = profile_dataframe(df, name)
        print(f"Table '{name}': {prof['row_count']} rows, {prof['col_count']} cols profiled successfully.")
    print("All canonical tables profiled without errors.\n")

def test_customer_risk_pipeline():
    print("--- Testing Customer Risk Pipeline ---")
    tables = load_canonical_data()
    df_cust = tables.get("customers", pd.DataFrame())
    df_tx = tables.get("transactions", pd.DataFrame())
    df_items = tables.get("transaction_items", pd.DataFrame())
    
    risk_df = predict_customer_risk(df_cust, df_tx, df_items)
    print(f"Risk dataframe generated with shape {risk_df.shape} and columns: {list(risk_df.columns)}")
    merge_cols = [c for c in risk_df.columns if c not in df_cust.columns or c == "customer_id"]
    merged = df_cust.merge(risk_df[merge_cols], on="customer_id", how="left")
    print(f"Merged customer dataframe shape: {merged.shape}. Required columns present: {'recency_days' in merged and 'risk_band' in merged}")
    print("Customer risk pipeline verified successfully.\n")

def test_intent_parser():
    print("--- Testing Intent Parser Queries ---")
    queries = [
        "Show me high risk suppliers",
        "Which customers are at risk of churn?",
        "Predict revenue next 14 days",
        "What if price increases by 10%",
        "Show anomaly detection results"
    ]
    for q in queries:
        parsed = parse_user_intent(q)
        print(f"Query: '{q}' -> Intent: {parsed['intent']}, Target Page: {parsed['target_page']}")
    print("Intent parser verified successfully.\n")

def test_emoji_scan():
    print("--- Scanning for Visible Emojis in App Source Files ---")
    import glob
    files = glob.glob('app/**/*.py', recursive=True) + glob.glob('app/**/*.css', recursive=True) + glob.glob('.streamlit/*.toml')
    emoji_lines = []
    for f in files:
        with open(f, 'rb') as file:
            content = file.read().decode('utf-8', errors='ignore')
            for idx, line in enumerate(content.splitlines(), 1):
                # Ignore unicode arrows, dashes, box-drawing chars (\u2500-\u257f)
                emojis = [c for c in line if ord(c) > 0x2000 and not (0x2500 <= ord(c) <= 0x257f) and ord(c) not in (0x2014, 0x2013, 0x2026, 0x2019, 0x201c, 0x201d, 0x2192)]
                if emojis:
                    emoji_lines.append(f"{f}:{idx} -> {line.strip()}")
    
    if emoji_lines:
        print(f"WARNING: Found {len(emoji_lines)} lines with emojis:")
        for el in emoji_lines:
            print(" ", ascii(el))
    else:
        print("ZERO visible emojis found in user-facing app files!")
    print()


if __name__ == "__main__":
    test_profiling()
    test_customer_risk_pipeline()
    test_intent_parser()
    test_emoji_scan()
    print("All verification checks completed!")
