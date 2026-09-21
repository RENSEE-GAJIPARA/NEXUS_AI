"""Time-Series Forecasting Engine for NEXUS AI Demand & Revenue."""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.ensemble import GradientBoostingRegressor
from src.features.time_features import build_daily_time_series_features
from src.models.evaluation import evaluate_regression
from src.models.registry import save_model_artifact, load_model_artifact
from src.utils.logging import logger

FORECAST_FEATURES = ["lag_1", "lag_7", "lag_14", "lag_30", "rolling_mean_7", "rolling_mean_14", "rolling_std_7", "day_of_week", "month", "is_weekend"]

def train_forecasting_model(df_transactions: pd.DataFrame):
    """Train Gradient Boosting time-series forecaster with chronological split."""
    daily = build_daily_time_series_features(df_transactions)
    daily_clean = daily.dropna(subset=FORECAST_FEATURES).copy()
    
    if len(daily_clean) < 60:
        logger.warning("Insufficient historical dates for forecaster training.")
        return None
        
    # Chronological Split (80% train, 20% test)
    split_idx = int(len(daily_clean) * 0.8)
    train_df = daily_clean.iloc[:split_idx]
    test_df = daily_clean.iloc[split_idx:]
    
    X_train, y_train = train_df[FORECAST_FEATURES], train_df["daily_revenue"]
    X_test, y_test = test_df[FORECAST_FEATURES], test_df["daily_revenue"]
    
    # Baseline comparison: Naive (lag_1)
    naive_preds = X_test["lag_1"]
    naive_metrics = evaluate_regression(y_test, naive_preds)
    
    # ML Model
    gbr = GradientBoostingRegressor(n_estimators=100, learning_rate=0.05, max_depth=4, random_state=42)
    gbr.fit(X_train, y_train)
    
    ml_preds = gbr.predict(X_test)
    ml_metrics = evaluate_regression(y_test, ml_preds)
    
    logger.info(f"Forecast Model Metrics -> Naive MAE: {naive_metrics['mae']}, GBR MAE: {ml_metrics['mae']}")
    
    metadata = {
        "algorithm": "GradientBoostingRegressor",
        "features": FORECAST_FEATURES,
        "metrics": ml_metrics,
        "baseline_naive_metrics": naive_metrics,
        "train_size": len(train_df),
        "test_size": len(test_df)
    }
    save_model_artifact("demand_forecast_model", gbr, metadata)
    return gbr

def generate_multi_step_forecast(df_transactions: pd.DataFrame, horizon_days: int = 14) -> pd.DataFrame:
    """Generate forward N-day revenue forecast with confidence bounds."""
    daily = build_daily_time_series_features(df_transactions)
    model, metadata = load_model_artifact("demand_forecast_model")
    
    if model is None:
        model = train_forecasting_model(df_transactions)
        
    history = daily.copy()
    last_date = pd.to_datetime(history["transaction_date"].max())
    
    forecasts = []
    
    # Recursive multi-step forecasting
    for i in range(1, horizon_days + 1):
        next_date = last_date + timedelta(days=i)
        
        # Calculate lag features from current history
        revs = history["daily_revenue"].values
        lag_1 = revs[-1] if len(revs) >= 1 else 0
        lag_7 = revs[-7] if len(revs) >= 7 else lag_1
        lag_14 = revs[-14] if len(revs) >= 14 else lag_1
        lag_30 = revs[-30] if len(revs) >= 30 else lag_1
        
        roll_mean_7 = np.mean(revs[-7:]) if len(revs) >= 7 else lag_1
        roll_mean_14 = np.mean(revs[-14:]) if len(revs) >= 14 else lag_1
        roll_std_7 = np.std(revs[-7:]) if len(revs) >= 7 else 0.0
        
        feat_vector = pd.DataFrame([{
            "lag_1": lag_1,
            "lag_7": lag_7,
            "lag_14": lag_14,
            "lag_30": lag_30,
            "rolling_mean_7": roll_mean_7,
            "rolling_mean_14": roll_mean_14,
            "rolling_std_7": roll_std_7,
            "day_of_week": next_date.dayofweek,
            "month": next_date.month,
            "is_weekend": 1 if next_date.dayofweek >= 5 else 0
        }])
        
        pred_rev = float(model.predict(feat_vector)[0])
        pred_rev = max(0.0, pred_rev) # Non-negative constraint
        
        std_err = metadata.get("metrics", {}).get("mae", pred_rev * 0.1)
        lower_bound = max(0.0, pred_rev - 1.96 * std_err)
        upper_bound = pred_rev + 1.96 * std_err
        
        forecasts.append({
            "date": next_date.strftime("%Y-%m-%d"),
            "forecasted_revenue": round(pred_rev, 2),
            "lower_bound": round(lower_bound, 2),
            "upper_bound": round(upper_bound, 2)
        })
        
        # Append to history for next recursive step
        new_row = pd.DataFrame([{"transaction_date": next_date.strftime("%Y-%m-%d"), "daily_revenue": pred_rev}])
        history = pd.concat([history, new_row], ignore_index=True)
        
    return pd.DataFrame(forecasts)
