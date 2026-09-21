# METHODOLOGY & STATISTICAL FOUNDATIONS — NEXUS AI

NEXUS AI integrates multi-disciplinary data engineering, machine learning, and graph algorithms into a coherent decision-support framework.

## 1. Data Validation & Quality Score Metric
Data Quality Score is calculated dynamically as:
$$\text{Quality Score} = \frac{\sum \text{Passed Audits}}{\text{Total Automated Audits}} \times 100\%$$
Audits verify completeness ($\ge 95\%$), uniqueness ($\ge 99\%$), domain validity (non-negative monetary values, valid quantities), and referential integrity across relational tables.

## 2. Customer Risk Scoring Methodology
Customer churn risk uses RFM feature transformation combined with an explicit proxy churn label:
$$\text{Proxy Churn} = \mathbb{I}(\text{Recency Days} > 60)$$
Risk probabilities from Gradient Boosting classifiers are segmented into 3 operational risk bands:
- **Low Risk**: $P(\text{Churn}) < 0.40$
- **Medium Risk**: $0.40 \le P(\text{Churn}) < 0.70$
- **High Risk**: $P(\text{Churn}) \ge 0.70$

## 3. Isolation Forest Anomaly Detection
Outlier scores from Isolation Forest are normalized via min-max scaling:
$$S_{\text{norm}}(x) = 1.0 - \frac{S(x) - S_{\min}}{S_{\max} - S_{\min}}$$
Flagged records ($S_{\text{norm}} \ge 0.75$) generate deterministic explanations identifying feature values exceeding standard deviation thresholds.

## 4. Time-Series Forecasting
Forecasting uses recursive multi-step autoregressive features:
$$y_{t} = f\Big(y_{t-1}, y_{t-7}, y_{t-14}, \mu_{t-7}(y), \sigma_{t-7}(y), \text{Calendar Encodings}\Big)$$
Model evaluation uses Chronological Splits to prevent data leakage. Confidence bounds represent 95% standard error intervals:
$$\text{CI}_{95\%} = \hat{y} \pm 1.96 \times \text{MAE}$$

## 5. What-If Price Elasticity Simulation
Simulated demand incorporates Price Elasticity of Demand ($\epsilon = -1.2$):
$$\% \Delta Q = \epsilon \cdot \% \Delta P + 0.8 \cdot \% \Delta \text{Discount}$$
$$Q_{\text{sim}} = Q_{\text{base}} \times (1 + \% \Delta Q) \times \min\Big(\text{InvFactor}, \frac{\text{SupAvail}}{100}\Big)$$
$$\text{Revenue}_{\text{sim}} = \text{Revenue}_{\text{base}} \times \left(\frac{Q_{\text{sim}}}{Q_{\text{base}}}\right) \times (1 + \% \Delta P)(1 - \% \Delta \text{Discount})$$

## 6. Disclaimers & Ethics
- **Decision Support Only**: Model predictions provide analytical guidance; human operational oversight is mandatory.
- **Zero Paid API Requirement**: Natural language query understanding uses localized intent matching with zero paid LLM dependencies.
