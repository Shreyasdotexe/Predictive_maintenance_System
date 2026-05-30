"""
Data loading, feature engineering, and model training for the predictive
maintenance pipeline.  Everything is wrapped behind Streamlit caching so
the heavy work only runs once per session (or when the underlying data
changes).
"""

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


DATA_PATH = "machinery_data.csv"

FEATURE_COLS = [
    "sensor_1", "sensor_2", "sensor_3",
    "operational_hours", "sensor_avg", "sensor_diff",
]


@st.cache_data(show_spinner="Loading machinery data...")
def load_data():
    """Read the CSV and add derived features we need downstream."""
    df = pd.read_csv(DATA_PATH)
    # forward-fill to handle any sensor gaps in the time series
    df.ffill(inplace=True)

    df["sensor_avg"]  = df[["sensor_1", "sensor_2", "sensor_3"]].mean(axis=1)
    df["sensor_diff"] = df["sensor_1"] - df["sensor_2"]
    return df


@st.cache_resource(show_spinner="Training models (this only runs once)...")
def train_models(_df: pd.DataFrame):
    """
    Fit the three models on the full dataset and return them together
    with the fitted scaler.

    The leading underscore in `_df` tells Streamlit not to hash this
    argument (DataFrames are expensive to hash).
    """
    df = _df.copy()
    scaler = StandardScaler()
    df[FEATURE_COLS] = scaler.fit_transform(df[FEATURE_COLS])

    X = df[FEATURE_COLS]

    rul_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
    rul_model.fit(X, df["RUL"])

    maint_model = GradientBoostingClassifier(n_estimators=100, random_state=42)
    maint_model.fit(X, df["maintenance"])

    anomaly_model = KMeans(n_clusters=2, random_state=42, n_init=10)
    anomaly_model.fit(X)

    return scaler, rul_model, maint_model, anomaly_model


def predict(scaler, rul_model, maint_model, anomaly_model,
            sensor_1, sensor_2, sensor_3, op_hours):
    """Run a single prediction through all three models."""
    sensor_avg  = (sensor_1 + sensor_2 + sensor_3) / 3
    sensor_diff = sensor_1 - sensor_2

    row = np.array([[sensor_1, sensor_2, sensor_3,
                     op_hours, sensor_avg, sensor_diff]])
    row_scaled = scaler.transform(row)

    rul         = rul_model.predict(row_scaled)[0]
    maintenance = maint_model.predict(row_scaled)[0]
    cluster     = anomaly_model.predict(row_scaled)[0]

    return rul, int(maintenance), int(cluster)
