"""Business Insight Synthesis Engine for NEXUS AI."""
import pandas as pd
from typing import Dict, List, Any

def generate_supplier_risk_insight(supplier_row: pd.Series, graph_conn_count: int = 0) -> str:
    """Generate grounded natural language insight for a supplier."""
    sup_id = supplier_row.get("supplier_id", "Unknown")
    sup_name = supplier_row.get("supplier_name", sup_id)
    delay_rate = supplier_row.get("delay_rate", 0.0)
    rel_score = supplier_row.get("reliability_score", 1.0)
    risk_score = supplier_row.get("composite_supplier_risk", 0.0)
    
    status = "Elevated Operational Risk" if risk_score > 0.40 else "Stable Operational Performance"
    
    insight = (
        f"Supplier '{sup_name}' ({sup_id}) exhibits {status.lower()} (Risk Score: {risk_score:.2f}). "
        f"It maintains a historical delay rate of {delay_rate:.1%} and a reliability score of {rel_score:.0%}. "
        f"Graph analysis indicates dependency links across {graph_conn_count} downstream customer touchpoints."
    )
    return insight

def generate_customer_risk_insight(customer_row: pd.Series) -> str:
    """Generate grounded natural language insight for customer churn risk."""
    c_id = customer_row.get("customer_id", "Unknown")
    prob = customer_row.get("risk_probability", 0.0)
    rec = customer_row.get("recency_days", 0)
    band = customer_row.get("risk_band", "Low")
    
    insight = (
        f"Customer '{c_id}' is classified as {band} Churn Risk (Probability: {prob:.1%}). "
        f"The customer has been inactive for {int(rec)} days. "
    )
    if rec > 60:
        insight += "Inactivity exceeds the standard 60-day operational retention threshold."
    else:
        insight += "Customer remains within expected purchasing cadence."
    return insight
