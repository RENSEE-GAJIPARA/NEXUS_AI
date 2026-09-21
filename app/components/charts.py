"""Plotly Chart Visualizations for NEXUS AI."""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

PLOTLY_LIGHT_LAYOUT = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "#FFFFFF",
    "font": {"color": "#172033", "family": "Inter, sans-serif"},
    "xaxis": {"gridcolor": "#E2E8F0", "zerolinecolor": "#CBD5E1"},
    "yaxis": {"gridcolor": "#E2E8F0", "zerolinecolor": "#CBD5E1"},
    "margin": {"l": 40, "r": 40, "t": 40, "b": 40}
}

def plot_line_chart(df: pd.DataFrame, x_col: str, y_col: str, title: str, color_col: str = None) -> go.Figure:
    """Line chart for temporal trends."""
    fig = px.line(df, x=x_col, y=y_col, color=color_col, title=title, color_discrete_sequence=["#2563EB", "#16A34A", "#D97706"])
    fig.update_layout(**PLOTLY_LIGHT_LAYOUT)
    fig.update_traces(line=dict(width=2.5))
    return fig

def plot_bar_chart(df: pd.DataFrame, x_col: str, y_col: str, title: str, orientation: str = "v") -> go.Figure:
    """Bar chart for categorical breakdowns."""
    fig = px.bar(df, x=x_col, y=y_col, title=title, orientation=orientation, color_discrete_sequence=["#2563EB"])
    fig.update_layout(**PLOTLY_LIGHT_LAYOUT)
    return fig

def plot_forecast_chart(historical_df: pd.DataFrame, forecast_df: pd.DataFrame, title: str = "14-Day Demand & Revenue Forecast") -> go.Figure:
    """Plot historical sales line alongside future predictions and confidence intervals."""
    fig = go.Figure()
    
    # Historical
    fig.add_trace(go.Scatter(
        x=historical_df["date"], y=historical_df["revenue"],
        name="Historical Revenue", line=dict(color="#2563EB", width=2.5)
    ))
    
    # Forecast
    fig.add_trace(go.Scatter(
        x=forecast_df["date"], y=forecast_df["forecasted_revenue"],
        name="Forecast", line=dict(color="#16A34A", width=3, dash="dash")
    ))
    
    # Confidence Interval Bounds
    fig.add_trace(go.Scatter(
        x=forecast_df["date"].tolist() + forecast_df["date"].tolist()[::-1],
        y=forecast_df["upper_bound"].tolist() + forecast_df["lower_bound"].tolist()[::-1],
        fill="toself", fillcolor="rgba(22, 163, 74, 0.12)",
        line=dict(color="rgba(255,255,255,0)"),
        name="95% Confidence Interval"
    ))
    
    fig.update_layout(**PLOTLY_LIGHT_LAYOUT)
    fig.update_layout(title=title)
    return fig

def plot_donut_chart(labels: list, values: list, title: str) -> go.Figure:
    """Donut chart for risk distributions."""
    fig = go.Figure(data=[go.Pie(
        labels=labels, values=values, hole=0.55,
        marker=dict(colors=["#16A34A", "#D97706", "#DC2626"])
    )])
    fig.update_layout(**PLOTLY_LIGHT_LAYOUT)
    fig.update_layout(title=title)
    return fig

