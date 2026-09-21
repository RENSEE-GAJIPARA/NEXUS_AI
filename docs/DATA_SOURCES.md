# DATA SOURCES & METADATA — NEXUS AI

| Dataset Name | Source | License | Row Count | Tables Included | Data Type | Role in NEXUS AI |
|---|---|---|---|---|---|---|
| **NEXUS Canonical Retail Graph** | NEXUS AI Data Pipeline | MIT / Public Domain | 72,564 total | `customers`, `products`, `suppliers`, `stores`, `locations`, `transactions`, `transaction_items`, `inventory`, `calendar` | Real/Cohesive Synthetic Hybrid | Core multi-entity relational dataset powering graph intelligence, churn risk, demand forecasting, anomaly detection, and scenario simulations. |

## Data Schema Overview

- **customers**: 500 records (`customer_id`, `age`, `gender`, `location_id`, `signup_date`, `customer_segment`)
- **suppliers**: 30 records (`supplier_id`, `supplier_name`, `location_id`, `lead_time`, `reliability_score`, `delay_rate`)
- **stores**: 20 records (`store_id`, `location_id`, `store_type`)
- **products**: 92 records (`product_id`, `product_name`, `category`, `subcategory`, `brand`, `supplier_id`, `unit_cost`, `unit_price`)
- **locations**: 10 records (`location_id`, `city`, `state`, `country`)
- **transactions**: 15,000 records (`transaction_id`, `customer_id`, `store_id`, `transaction_date`, `total_amount`, `payment_type`)
- **transaction_items**: 27,397 records (`transaction_id`, `product_id`, `quantity`, `unit_price`, `discount`, `item_total`)
- **inventory**: 29,200 records (`product_id`, `store_id`, `date`, `stock_level`, `reorder_point`, `stockout_risk`)
- **calendar**: 365 records (`date`, `day`, `month`, `quarter`, `year`, `week`, `weekday`, `is_weekend`, `is_holiday`)

## Data Ingestion & Quality Controls
All tables are validated dynamically using `src/data/validation.py` for completeness, referential integrity, domain range validity, and uniqueness.
