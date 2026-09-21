"""Time-Series Feature Engineering for NEXUS AI Demand Forecasting."""
import pandas as pd
import numpy as np

def build_daily_time_series_features(df_transactions: pd.DataFrame, group_col: str = None) -> pd.DataFrame:
    """Aggregate daily sales and generate lag features (1, 7, 14, 30 days) and rolling stats."""
    if df_transactions.empty:
        return pd.DataFrame()
        
    df = df_transactions.copy()
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    
    if group_col and group_col in df.columns:
        daily = df.groupby(["transaction_date", group_col]).agg(
            daily_revenue=("total_amount", "sum"),
            daily_orders=("transaction_id", "nunique")
        ).reset_index()
        daily = daily.sort_values(by=["transaction_date"])
        
        # Calculate lags per group
        for lag in [1, 7, 14, 30]:
            daily[f"lag_{lag}"] = daily.groupby(group_col)["daily_revenue"].shift(lag)
        for roll in [7, 14, 30]:
            daily[f"rolling_mean_{roll}"] = daily.groupby(group_col)["daily_revenue"].transform(lambda x: x.shift(1).rolling(roll).mean())
            daily[f"rolling_std_{roll}"] = daily.groupby(group_col)["daily_revenue"].transform(lambda x: x.shift(1).rolling(roll).std())
    else:
        daily = df.groupby("transaction_date").agg(
            daily_revenue=("total_amount", "sum"),
            daily_orders=("transaction_id", "nunique")
        ).reset_index()
        daily = daily.sort_values(by="transaction_date")
        
        for lag in [1, 7, 14, 30]:
            daily[f"lag_{lag}"] = daily["daily_revenue"].shift(lag)
        for roll in [7, 14, 30]:
            daily[f"rolling_mean_{roll}"] = daily["daily_revenue"].shift(1).rolling(roll).mean()
            daily[f"rolling_std_{roll}"] = daily["daily_revenue"].shift(1).rolling(roll).std()
            
    # Temporal encodings
    daily["day_of_week"] = daily["transaction_date"].dt.dayofweek
    daily["month"] = daily["transaction_date"].dt.month
    daily["is_weekend"] = (daily["day_of_week"] >= 5).astype(int)
    
    return daily
