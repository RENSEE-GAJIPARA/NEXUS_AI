"""Heterogeneous Business Relationship Graph Builder for NEXUS AI."""
import networkx as nx
import pandas as pd
from typing import Dict, Any
from src.utils.logging import logger

def build_business_graph(tables: Dict[str, pd.DataFrame], max_tx_sample: int = 2000) -> nx.Graph:
    """Construct multi-entity heterogeneous NetworkX business graph."""
    G = nx.Graph()
    
    # 1. Add Locations
    if "locations" in tables and not tables["locations"].empty:
        for _, row in tables["locations"].iterrows():
            G.add_node(row["location_id"], node_type="Location", name=row.get("city", row["location_id"]))
            
    # 2. Add Suppliers
    if "suppliers" in tables and not tables["suppliers"].empty:
        for _, row in tables["suppliers"].iterrows():
            sup_id = row["supplier_id"]
            G.add_node(sup_id, node_type="Supplier", name=row.get("supplier_name", sup_id), delay_rate=row.get("delay_rate", 0.0), reliability=row.get("reliability_score", 1.0))
            if "location_id" in row and row["location_id"] in G:
                G.add_edge(sup_id, row["location_id"], relation="LOCATED_IN")
                
    # 3. Add Stores
    if "stores" in tables and not tables["stores"].empty:
        for _, row in tables["stores"].iterrows():
            st_id = row["store_id"]
            G.add_node(st_id, node_type="Store", name=st_id, store_type=row.get("store_type", "Standard"))
            if "location_id" in row and row["location_id"] in G:
                G.add_edge(st_id, row["location_id"], relation="LOCATED_IN")
                
    # 4. Add Products
    if "products" in tables and not tables["products"].empty:
        for _, row in tables["products"].iterrows():
            p_id = row["product_id"]
            G.add_node(p_id, node_type="Product", name=row.get("product_name", p_id), category=row.get("category", "General"), price=row.get("unit_price", 0.0))
            if "supplier_id" in row and row["supplier_id"] in G:
                G.add_edge(p_id, row["supplier_id"], relation="SUPPLIED_BY")

    # 5. Add Customers
    if "customers" in tables and not tables["customers"].empty:
        for _, row in tables["customers"].iterrows():
            c_id = row["customer_id"]
            G.add_node(c_id, node_type="Customer", name=c_id, segment=row.get("customer_segment", "Standard"))
            if "location_id" in row and row["location_id"] in G:
                G.add_edge(c_id, row["location_id"], relation="RESIDES_IN")
                
    # 6. Add Customer-Product & Customer-Store interactions from Transactions (sample for high performance)
    if "transactions" in tables and "transaction_items" in tables:
        tx_sample = tables["transactions"].sample(n=min(len(tables["transactions"]), max_tx_sample), random_state=42)
        items_merged = tx_sample.merge(tables["transaction_items"], on="transaction_id", how="inner")
        
        for _, row in items_merged.iterrows():
            c_id = row["customer_id"]
            p_id = row["product_id"]
            st_id = row["store_id"]
            
            if c_id in G and p_id in G:
                if G.has_edge(c_id, p_id):
                    G[c_id][p_id]["weight"] += 1
                else:
                    G.add_edge(c_id, p_id, relation="BUYS_PRODUCT", weight=1)
                    
            if c_id in G and st_id in G:
                if G.has_edge(c_id, st_id):
                    G[c_id][st_id]["weight"] += 1
                else:
                    G.add_edge(c_id, st_id, relation="VISITS_STORE", weight=1)

    logger.info(f"Constructed business graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges.")
    return G
