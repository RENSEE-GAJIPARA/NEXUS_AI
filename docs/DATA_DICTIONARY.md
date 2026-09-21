# DATA DICTIONARY — NEXUS AI

| Table Name | Column Name | Data Type | Description | Sample Value |
|---|---|---|---|---|
| **customers** | `customer_id` | String | Unique customer identifier | `CUST_0001` |
| | `age` | Integer | Customer age in years | `34` |
| | `gender` | String | Customer gender category | `M` |
| | `location_id` | String | Foreign key to location | `LOC_01` |
| | `signup_date` | String | Account creation date (YYYY-MM-DD) | `2023-05-12` |
| | `customer_segment` | String | Marketing segment | `VIP` |
| **suppliers** | `supplier_id` | String | Unique supplier identifier | `SUP_001` |
| | `supplier_name` | String | Supplier corporate name | `Apex Global Supply` |
| | `lead_time` | Integer | Delivery lead time in days | `12` |
| | `reliability_score` | Float | Fulfillment reliability rating (0-1) | `0.95` |
| | `delay_rate` | Float | Historical shipment delay percentage | `0.08` |
| **products** | `product_id` | String | Unique product SKU identifier | `PRD_0001` |
| | `product_name` | String | Descriptive product title | `Brand_A Smartphones Model 1` |
| | `category` | String | High-level product category | `Electronics` |
| | `supplier_id` | String | Foreign key to supplier | `SUP_001` |
| | `unit_price` | Float | Retail selling price ($) | `299.99` |
| **transactions** | `transaction_id` | String | Unique transaction receipt ID | `TXN_000001` |
| | `customer_id` | String | Foreign key to customer | `CUST_0001` |
| | `store_id` | String | Foreign key to retail store | `STR_001` |
| | `transaction_date` | String | Transaction timestamp (YYYY-MM-DD) | `2025-06-15` |
| | `total_amount` | Float | Gross transaction monetary total ($) | `450.00` |
| **inventory** | `product_id` | String | Foreign key to product SKU | `PRD_0001` |
| | `store_id` | String | Foreign key to store location | `STR_001` |
| | `stock_level` | Integer | Units currently available in stock | `45` |
| | `reorder_point` | Integer | Minimum threshold for stock reordering | `20` |
| | `stockout_risk` | Integer | Flag (1 if stock_level <= reorder_point) | `0` |
