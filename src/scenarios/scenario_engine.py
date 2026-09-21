"""What-If Scenario Simulation Engine for NEXUS AI."""
import pandas as pd
import numpy as np
from typing import Dict, Any

def run_what_if_simulation(
    base_revenue: float,
    base_demand: float,
    price_change_pct: float = 0.0,
    discount_change_pct: float = 0.0,
    inventory_factor: float = 1.0,
    supplier_availability_pct: float = 100.0,
    price_elasticity: float = -1.2
) -> Dict[str, Any]:
    """Calculate model-based demand & revenue changes under altered business parameters.
    
    Price Elasticity of Demand formula: % Change in Qty = Elasticity * % Change in Price
    """
    # 1. Price adjustment impact
    effective_price_change = price_change_pct / 100.0
    demand_change_from_price = price_elasticity * effective_price_change
    
    # 2. Discount change impact (higher discount increases demand)
    effective_discount_change = discount_change_pct / 100.0
    demand_change_from_discount = 0.8 * effective_discount_change
    
    # 3. Combined demand elasticity multiplier
    net_demand_pct_change = demand_change_from_price + demand_change_from_discount
    
    # 4. Unconstrained simulated demand
    unconstrained_demand = base_demand * (1.0 + net_demand_pct_change)
    
    # 5. Supply constraint cap
    supplier_cap_factor = supplier_availability_pct / 100.0
    constrained_demand = unconstrained_demand * min(inventory_factor, supplier_cap_factor)
    
    # 6. Simulated revenue calculation
    price_multiplier = (1.0 + effective_price_change) * (1.0 - effective_discount_change)
    simulated_revenue = base_revenue * (constrained_demand / max(1.0, base_demand)) * price_multiplier
    
    rev_abs_diff = simulated_revenue - base_revenue
    rev_pct_diff = (rev_abs_diff / base_revenue) * 100.0 if base_revenue > 0 else 0.0
    
    demand_abs_diff = constrained_demand - base_demand
    demand_pct_diff = (demand_abs_diff / base_demand) * 100.0 if base_demand > 0 else 0.0
    
    return {
        "baseline_demand": round(float(base_demand), 2),
        "simulated_demand": round(float(constrained_demand), 2),
        "demand_abs_diff": round(float(demand_abs_diff), 2),
        "demand_pct_diff": round(float(demand_pct_diff), 2),
        "baseline_revenue": round(float(base_revenue), 2),
        "simulated_revenue": round(float(simulated_revenue), 2),
        "revenue_abs_diff": round(float(rev_abs_diff), 2),
        "revenue_pct_diff": round(float(rev_pct_diff), 2),
        "disclaimer": "Model-Based Scenario Simulation. Outputs represent estimated mathematical projections and do not guarantee causal real-world outcomes."
    }
