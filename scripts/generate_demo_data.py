"""Demo Data Generator for NEXUS AI.
Generates realistic, interconnected, relational business intelligence datasets.
Saved to data/processed/ and data/synthetic/.
"""
import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Ensure src modules are importable
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.utils.paths import DATA_PROCESSED_DIR, DATA_SYNTHETIC_DIR
from src.utils.logging import logger

def generate_nexus_data(seed: int = 42, num_customers: int = 500, num_products: int = 100):
    """Generate cohesive multi-entity business datasets."""
    np.random.seed(seed)
    os.makedirs(DATA_PROCESSED_DIR, exist_ok=True)
    os.makedirs(DATA_SYNTHETIC_DIR, exist_ok=True)
    
    logger.info("Generating canonical datasets for NEXUS AI...")
    
    # 1. Locations
    locations_data = [
        {"location_id": "LOC_01", "city": "New York", "state": "NY", "country": "USA"},
        {"location_id": "LOC_02", "city": "Los Angeles", "state": "CA", "country": "USA"},
        {"location_id": "LOC_03", "city": "Chicago", "state": "IL", "country": "USA"},
        {"location_id": "LOC_04", "city": "Houston", "state": "TX", "country": "USA"},
        {"location_id": "LOC_05", "city": "Phoenix", "state": "AZ", "country": "USA"},
        {"location_id": "LOC_06", "city": "Seattle", "state": "WA", "country": "USA"},
        {"location_id": "LOC_07", "city": "Miami", "state": "FL", "country": "USA"},
        {"location_id": "LOC_08", "city": "Boston", "state": "MA", "country": "USA"},
        {"location_id": "LOC_09", "city": "Denver", "state": "CO", "country": "USA"},
        {"location_id": "LOC_10", "city": "Atlanta", "state": "GA", "country": "USA"},
    ]
    df_locations = pd.DataFrame(locations_data)
    
    # 2. Suppliers
    suppliers = []
    supplier_names = [
        "Apex Global Supply", "Vortex Components", "Nexus Tech Logistics", "Titan Industrial",
        "Pinnacle Freight", "Zenith Electronics", "Aurora Fabrics", "Velocity Hardware",
        "Solstice Trading", "Echo Distribution", "Beacon Manufacturing", "Quantum Supply",
        "Orion Metals", "Nova Packaging", "Summit Microelectronics", "Atlas Chemicals",
        "Prism Plastics", "Omega Goods", "Starlight Materials", "Horizon Logistics",
        "Bravura Importers", "Crestview Wholesale", "Dynasty Trade Co", "Elevate Direct",
        "Frontier Supply", "Genesis Components", "Hyperion Products", "Infinity Tech",
        "Jubilee Distribution", "Keystone Freight"
    ]
    for i, name in enumerate(supplier_names):
        sup_id = f"SUP_{i+1:03d}"
        loc_id = np.random.choice(df_locations["location_id"])
        lead_time = int(np.random.randint(2, 21))
        reliability = round(float(np.random.uniform(0.70, 0.99)), 2)
        delay_rate = round(float(np.random.uniform(0.02, 0.25) if reliability > 0.85 else np.random.uniform(0.20, 0.45)), 2)
        suppliers.append({
            "supplier_id": sup_id,
            "supplier_name": name,
            "location_id": loc_id,
            "lead_time": lead_time,
            "reliability_score": reliability,
            "delay_rate": delay_rate
        })
    df_suppliers = pd.DataFrame(suppliers)
    
    # 3. Stores
    stores = []
    store_types = ["Flagship", "Superstore", "Express", "Outlet"]
    for i in range(1, 21):
        stores.append({
            "store_id": f"STR_{i:03d}",
            "location_id": np.random.choice(df_locations["location_id"]),
            "store_type": np.random.choice(store_types, p=[0.2, 0.4, 0.3, 0.1])
        })
    df_stores = pd.DataFrame(stores)
    
    # 4. Products
    categories = {
        "Electronics": ["Smartphones", "Laptops", "Audio", "Accessories", "Wearables"],
        "Apparel": ["Men's Wear", "Women's Wear", "Footwear", "Activewear", "Accessories"],
        "Home & Kitchen": ["Cookware", "Appliances", "Furniture", "Decor", "Bedding"],
        "Health & Personal": ["Skincare", "Vitamins", "Grooming", "Oral Care"],
        "Office Supplies": ["Stationery", "Ergonomics", "Printers", "Organization"]
    }
    products = []
    prod_idx = 1
    for cat, subcats in categories.items():
        for subcat in subcats:
            for _ in range(4): # 5 cats * 5 subcats * 4 = 100 products
                p_id = f"PRD_{prod_idx:04d}"
                sup_id = np.random.choice(df_suppliers["supplier_id"])
                unit_cost = round(float(np.random.uniform(10.0, 450.0)), 2)
                margin = np.random.uniform(1.2, 2.1)
                unit_price = round(unit_cost * margin, 2)
                brand = f"Brand_{chr(65 + (prod_idx % 26))}"
                products.append({
                    "product_id": p_id,
                    "product_name": f"{brand} {subcat} Model {prod_idx}",
                    "category": cat,
                    "subcategory": subcat,
                    "brand": brand,
                    "supplier_id": sup_id,
                    "unit_cost": unit_cost,
                    "unit_price": unit_price
                })
                prod_idx += 1
    df_products = pd.DataFrame(products)
    
    # 5. Customers
    start_signup = datetime(2023, 1, 1)
    customers = []
    segments = ["VIP", "Regular", "Occasional", "Budget"]
    genders = ["M", "F", "Other"]
    for i in range(1, num_customers + 1):
        c_id = f"CUST_{i:04d}"
        age = int(np.random.randint(18, 72))
        gender = np.random.choice(genders, p=[0.48, 0.48, 0.04])
        loc_id = np.random.choice(df_locations["location_id"])
        signup_days = np.random.randint(0, 700)
        signup_date = (start_signup + timedelta(days=int(signup_days))).strftime("%Y-%m-%d")
        segment = np.random.choice(segments, p=[0.15, 0.45, 0.25, 0.15])
        customers.append({
            "customer_id": c_id,
            "age": age,
            "gender": gender,
            "location_id": loc_id,
            "signup_date": signup_date,
            "customer_segment": segment
        })
    df_customers = pd.DataFrame(customers)
    
    # 6. Calendar & Time series transactions setup
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 12, 31)
    date_range = pd.date_range(start_date, end_date)
    
    calendar_data = []
    for dt in date_range:
        calendar_data.append({
            "date": dt.strftime("%Y-%m-%d"),
            "day": dt.day,
            "month": dt.month,
            "quarter": dt.quarter,
            "year": dt.year,
            "week": dt.isocalendar().week,
            "weekday": dt.strftime("%A"),
            "is_weekend": 1 if dt.weekday() >= 5 else 0,
            "is_holiday": 1 if (dt.month == 12 and dt.day >= 24) or (dt.month == 7 and dt.day == 4) or (dt.month == 11 and dt.day >= 22 and dt.day <= 28) else 0
        })
    df_calendar = pd.DataFrame(calendar_data)
    
    # 7. Transactions & Transaction Items
    num_tx = 15000
    transactions = []
    tx_items = []
    
    # Select active customer distribution to generate churn behavior
    active_customers = df_customers["customer_id"].tolist()
    churned_pool = set(np.random.choice(active_customers, size=int(len(active_customers)*0.22), replace=False))
    
    dates_list = df_calendar["date"].tolist()
    payment_types = ["Credit Card", "Debit Card", "Digital Wallet", "Cash"]
    
    item_id_counter = 1
    for t_idx in range(1, num_tx + 1):
        tx_id = f"TXN_{t_idx:06d}"
        
        # Date selection with slight seasonal volume boost in Q4
        dt_str = np.random.choice(dates_list)
        dt_obj = datetime.strptime(dt_str, "%Y-%m-%d")
        
        # Churned customers do not buy after July 2025
        cust_id = np.random.choice(active_customers)
        if cust_id in churned_pool and dt_obj > datetime(2025, 7, 1):
            # Pick a non-churned customer
            cust_id = np.random.choice([c for c in active_customers if c not in churned_pool])
            
        store_id = np.random.choice(df_stores["store_id"])
        payment = np.random.choice(payment_types, p=[0.55, 0.25, 0.15, 0.05])
        
        # Determine items in transaction (1 to 5)
        num_items = np.random.choice([1, 2, 3, 4, 5], p=[0.5, 0.3, 0.1, 0.07, 0.03])
        sampled_prods = df_products.sample(n=num_items)
        
        tx_total = 0.0
        for _, prod in sampled_prods.iterrows():
            qty = int(np.random.choice([1, 2, 3, 4, 10], p=[0.7, 0.2, 0.06, 0.03, 0.01]))
            disc = float(np.random.choice([0.0, 0.05, 0.10, 0.15, 0.25], p=[0.6, 0.2, 0.1, 0.07, 0.03]))
            
            # Anomaly injection (~3% of items)
            if np.random.rand() < 0.008:
                qty = int(np.random.randint(40, 100)) # Unusually high quantity
            if np.random.rand() < 0.008:
                disc = 0.70 # Extreme discount
                
            unit_price = float(prod["unit_price"])
            item_total = round(qty * unit_price * (1.0 - disc), 2)
            tx_total += item_total
            
            tx_items.append({
                "transaction_id": tx_id,
                "product_id": prod["product_id"],
                "quantity": qty,
                "unit_price": unit_price,
                "discount": disc,
                "item_total": item_total
            })
            item_id_counter += 1
            
        # Transaction anomaly injection (~1% of transactions)
        if np.random.rand() < 0.005:
            tx_total = round(tx_total * 8.5, 2) # Anomalous total amount
            
        transactions.append({
            "transaction_id": tx_id,
            "customer_id": cust_id,
            "store_id": store_id,
            "transaction_date": dt_str,
            "total_amount": round(tx_total, 2),
            "payment_type": payment
        })
        
    df_transactions = pd.DataFrame(transactions)
    df_tx_items = pd.DataFrame(tx_items)
    
    # 8. Inventory Data (Sampled daily inventory across products and stores)
    inventory = []
    sample_dates = df_calendar["date"].unique()[::5] # Every 5 days to keep size optimal
    sample_stores = df_stores["store_id"].unique()[:10] # Top 10 stores
    
    for dt_str in sample_dates:
        for st_id in sample_stores:
            for p_id in df_products["product_id"].unique()[:40]: # Top 40 products
                stock = int(np.random.randint(5, 250))
                reorder = int(np.random.randint(20, 50))
                inventory.append({
                    "product_id": p_id,
                    "store_id": st_id,
                    "date": dt_str,
                    "stock_level": stock,
                    "reorder_point": reorder,
                    "stockout_risk": 1 if stock <= reorder else 0
                })
    df_inventory = pd.DataFrame(inventory)
    
    # Save canonical tables
    tables = {
        "locations": df_locations,
        "suppliers": df_suppliers,
        "stores": df_stores,
        "products": df_products,
        "customers": df_customers,
        "calendar": df_calendar,
        "transactions": df_transactions,
        "transaction_items": df_tx_items,
        "inventory": df_inventory
    }
    
    for t_name, df_table in tables.items():
        csv_path = DATA_PROCESSED_DIR / f"{t_name}.csv"
        df_table.to_csv(csv_path, index=False)
        try:
            pq_path = DATA_PROCESSED_DIR / f"{t_name}.parquet"
            df_table.to_parquet(pq_path, index=False)
        except Exception:
            pass # Parquet optional if pyarrow not installed
        logger.info(f"Saved dataset '{t_name}' -> {len(df_table)} rows.")
        
    # Document synthetic tag in synthetic folder
    syn_meta = pd.DataFrame([{"generated_at": datetime.now().isoformat(), "is_synthetic": True, "status": "DEMO_READY"}])
    syn_meta.to_json(DATA_SYNTHETIC_DIR / "metadata.json", orient="records")
    
    logger.info("Successfully generated all NEXUS AI datasets.")
    return tables

if __name__ == "__main__":
    generate_nexus_data()
