"""
Plotly chart builders for the dashboard.  Each function returns a
plotly Figure that the caller can pass straight to `st.plotly_chart()`.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


# -- colour palette (consistent across all charts) ----------------------------
PALETTE = {
    "primary":    "#feca57",   # gold accent
    "bg_dark":    "#2c3e50",
    "bg_mid":     "#3b5669",
    "text":       "#ecf0f1",
    "safe":       "#2ecc71",
    "warning":    "#f39c12",
    "danger":     "#e74c3c",
    "blue":       "#3498db",
    "purple":     "#9b59b6",
}

_CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color=PALETTE["text"],
    margin=dict(l=30, r=30, t=40, b=30),
)


def sensor_distributions(df: pd.DataFrame):
    """Overlaid histograms of the three raw sensor readings."""
    fig = go.Figure()
    colours = [PALETTE["blue"], PALETTE["primary"], PALETTE["purple"]]
    for col, colour in zip(["sensor_1", "sensor_2", "sensor_3"], colours):
        fig.add_trace(go.Histogram(
            x=df[col], name=col.replace("_", " ").title(),
            marker_color=colour, opacity=0.65,
        ))
    fig.update_layout(
        title="Sensor Reading Distributions",
        barmode="overlay", xaxis_title="Value", yaxis_title="Count",
        legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5),
        **_CHART_LAYOUT,
    )
    return fig


def rul_distribution(df: pd.DataFrame):
    """Histogram of Remaining Useful Life values across the fleet."""
    fig = px.histogram(
        df, x="RUL", nbins=40,
        color_discrete_sequence=[PALETTE["safe"]],
        title="RUL Distribution Across Machines",
    )
    fig.update_layout(
        xaxis_title="Remaining Useful Life (hrs)",
        yaxis_title="Count",
        **_CHART_LAYOUT,
    )
    return fig


def maintenance_breakdown(df: pd.DataFrame):
    """Donut chart: what fraction of records flagged maintenance."""
    counts = df["maintenance"].value_counts().reset_index()
    counts.columns = ["status", "count"]
    counts["status"] = counts["status"].map({0: "Normal", 1: "Needs Maintenance"})

    fig = px.pie(
        counts, values="count", names="status",
        color="status",
        color_discrete_map={
            "Normal": PALETTE["safe"],
            "Needs Maintenance": PALETTE["danger"],
        },
        hole=0.45,
        title="Maintenance Status Breakdown",
    )
    fig.update_layout(**_CHART_LAYOUT)
    fig.update_traces(textinfo="percent+label", textfont_color="white")
    return fig


def correlation_heatmap(df: pd.DataFrame):
    """Pearson correlation between the numeric columns."""
    cols = ["sensor_1", "sensor_2", "sensor_3", "operational_hours", "RUL"]
    corr = df[cols].corr()

    fig = go.Figure(data=go.Heatmap(
        z=corr.values, x=cols, y=cols,
        colorscale="Tealgrn", zmin=-1, zmax=1,
        text=np.round(corr.values, 2), texttemplate="%{text}",
        textfont=dict(color="white"),
    ))
    fig.update_layout(title="Feature Correlation Matrix", **_CHART_LAYOUT)
    return fig


def feature_importance(model, feature_names: list):
    """Horizontal bar chart of Gradient Boosting feature importances."""
    importances = model.feature_importances_
    order = np.argsort(importances)

    fig = go.Figure(go.Bar(
        x=importances[order],
        y=[feature_names[i].replace("_", " ").title() for i in order],
        orientation="h",
        marker_color=PALETTE["primary"],
    ))
    fig.update_layout(
        title="Feature Importance (RUL Model)",
        xaxis_title="Importance",
        **_CHART_LAYOUT,
    )
    return fig


def hours_vs_rul(df: pd.DataFrame):
    """Scatter plot showing how operational hours relate to remaining life."""
    fig = px.scatter(
        df, x="operational_hours", y="RUL",
        color="maintenance",
        color_discrete_map={0: PALETTE["blue"], 1: PALETTE["danger"]},
        opacity=0.6,
        title="Operational Hours vs Remaining Useful Life",
        labels={
            "operational_hours": "Operational Hours",
            "RUL": "Remaining Useful Life (hrs)",
            "maintenance": "Maintenance Flag",
        },
    )
    fig.update_layout(**_CHART_LAYOUT)
    return fig


def rul_gauge(rul_value: float, max_rul: float = 5000):
    """Gauge chart that visually shows how much life is left."""
    pct = max(0, min(rul_value / max_rul, 1.0))

    if pct > 0.6:
        bar_color = PALETTE["safe"]
    elif pct > 0.3:
        bar_color = PALETTE["warning"]
    else:
        bar_color = PALETTE["danger"]

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=rul_value,
        number=dict(suffix=" hrs", font_size=28),
        title=dict(text="Remaining Useful Life", font_size=16),
        gauge=dict(
            axis=dict(range=[0, max_rul], tickcolor=PALETTE["text"]),
            bar=dict(color=bar_color),
            bgcolor=PALETTE["bg_dark"],
            bordercolor=PALETTE["bg_mid"],
            steps=[
                dict(range=[0, max_rul * 0.3], color="rgba(231,76,60,0.15)"),
                dict(range=[max_rul * 0.3, max_rul * 0.6], color="rgba(243,156,18,0.15)"),
                dict(range=[max_rul * 0.6, max_rul], color="rgba(46,204,113,0.15)"),
            ],
        ),
    ))
    fig.update_layout(
        height=260,
        paper_bgcolor="rgba(0,0,0,0)",
        font_color=PALETTE["text"],
        margin=dict(l=30, r=30, t=50, b=10),
    )
    return fig
