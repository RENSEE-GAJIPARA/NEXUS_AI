# MODEL CARDS — NEXUS AI

## 1. Customer Churn Risk Model (`customer_risk_model`)
- **Objective**: Predict customer churn risk probability to enable proactive retention targeting.
- **Target Definition**: Proxy Churn Target (`1` if customer inactivity > 60 days from reference date, else `0`).
- **Algorithm**: Gradient Boosting Classifier (`scikit-learn`).
- **Input Features**: `age`, `recency_days`, `frequency`, `monetary_total`, `avg_order_value`, `product_diversity`, `tenure_days`.
- **Validation Metrics**: F1-Score: `0.9818`, ROC-AUC: `0.9996`, Accuracy: `0.9821`.
- **Intended Use**: Operational risk decision-support dashboard for customer success managers.
- **Inappropriate Use**: Automated account cancellation or punitive customer treatment.

---

## 2. Multi-Dimensional Anomaly Detector (`anomaly_model`)
- **Objective**: Identify statistical multi-variable transaction outliers.
- **Algorithm**: Isolation Forest (`scikit-learn`).
- **Features**: `total_amount`, `total_items`, `max_discount`, `avg_item_price`.
- **Contamination Target**: `3.0%`.
- **Output**: Normalized anomaly score (0.0 to 1.0) and empirical explanations.
- **Intended Use**: Highlighting suspicious transactions for manual audit review.

---

## 3. Demand & Revenue Forecaster (`demand_forecast_model`)
- **Objective**: Predict N-day forward revenue horizons (7, 14, 30 days).
- **Algorithm**: Recursive Multi-Step Gradient Boosting Regressor.
- **Validation**: Chronological split (80% train, 20% test).
- **Metrics**: MAE: `$17,235.05`, SMAPE: `14.2%`.
- **Intended Use**: Inventory stocking and financial cash-flow planning.

---

## 4. PyTorch GraphSAGE Node Classifier (`graph_model`)
- **Objective**: Heterogeneous graph node risk aggregator.
- **Algorithm**: 2-Layer PyTorch GraphSAGE aggregator.
- **Accuracy**: `98.62%` training node accuracy.
