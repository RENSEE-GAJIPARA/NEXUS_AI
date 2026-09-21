"""Natural Language Intent Parser for NEXUS AI (Zero Paid API Engine)."""
import re
from typing import Dict, Any

INTENT_PATTERNS = {
    "supplier_risk": [r"supplier", r"vendor", r"supply chain", r"lead time", r"delivery delay", r"reliability"],
    "customer_risk": [r"customer", r"churn", r"retention", r"at-risk", r"inactive", r"rfm"],
    "product_demand": [r"product", r"demand", r"stockout", r"bestseller", r"inventory", r"top sales"],
    "forecasting": [r"forecast", r"predict", r"future sales", r"revenue next", r"trend", r"days demand"],
    "anomalies": [r"anomal", r"outlier", r"unusual", r"flagged", r"abnormal", r"suspicious"],
    "graph_relationship": [r"graph", r"network", r"connection", r"dependency", r"cluster", r"topology"],
    "scenario_simulation": [r"what if", r"scenario", r"price change", r"discount change", r"simulation", r"sensitivity"],
    "data_quality": [r"data quality", r"missing values", r"duplicates", r"health score", r"validation", r"schema"]
}

PAGE_ROUTING = {
    "supplier_risk": "Supplier Intelligence",
    "customer_risk": "Customer Intelligence",
    "product_demand": "Product Intelligence",
    "forecasting": "Forecast Center",
    "anomalies": "Anomaly Detection",
    "graph_relationship": "Graph Intelligence",
    "scenario_simulation": "Scenario Lab",
    "data_quality": "Data Quality"
}

def parse_user_intent(query: str) -> Dict[str, Any]:
    """Parse user natural language prompt into matched intent and recommended page."""
    if not query or not query.strip():
        return {"intent": "executive_overview", "confidence": 1.0, "target_page": "Executive Overview"}
        
    q_clean = query.lower().strip()
    
    matches = {}
    for intent, patterns in INTENT_PATTERNS.items():
        count = 0
        for pattern in patterns:
            if re.search(pattern, q_clean):
                count += 1
        if count > 0:
            matches[intent] = count
            
    if not matches:
        return {
            "intent": "general_search",
            "confidence": 0.5,
            "target_page": "Executive Overview",
            "extracted_query": query
        }
        
    best_intent = max(matches, key=matches.get)
    confidence = min(1.0, 0.4 + matches[best_intent] * 0.3)
    
    return {
        "intent": best_intent,
        "confidence": confidence,
        "target_page": PAGE_ROUTING.get(best_intent, "Executive Overview"),
        "extracted_query": query
    }
