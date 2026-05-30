import streamlit as st
import pandas as pd

from models import load_data, train_models, predict, FEATURE_COLS
from visualizations import (
    sensor_distributions, rul_distribution, maintenance_breakdown,
    correlation_heatmap, feature_importance, hours_vs_rul, rul_gauge,
)
from styles import inject_css

# -- page setup ---------------------------------------------------------------
st.set_page_config(
    page_title="Predictive Maintenance Dashboard",
    page_icon="PM",
    layout="wide",
)
inject_css()

# -- data & models (cached, runs once) ----------------------------------------
raw_df = load_data()
scaler, rul_model, maint_model, anomaly_model = train_models(raw_df)

# -- sidebar -------------------------------------------------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Overview", "Predict", "Explore Data", "About"],
    label_visibility="collapsed",
)


# ======================================================================
#  OVERVIEW
# ======================================================================
if page == "Overview":

    # hero banner
    st.markdown("""
    <div class="hero-card">
        <h1>Predictive Maintenance Dashboard</h1>
        <p>Real-time failure prediction and anomaly detection for industrial machinery</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")  # spacer

    # KPI row
    total      = len(raw_df)
    avg_rul    = raw_df["RUL"].mean()
    maint_rate = raw_df["maintenance"].mean() * 100

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="stat-card">
            <h2>{total:,}</h2>
            <p>Records Analyzed</p>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="stat-card">
            <h2>{avg_rul:,.0f} hrs</h2>
            <p>Average Remaining Life</p>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="stat-card">
            <h2>{maint_rate:.1f}%</h2>
            <p>Maintenance Flag Rate</p>
        </div>""", unsafe_allow_html=True)

    st.write("")

    # two-column chart layout
    left, right = st.columns(2)
    with left:
        st.plotly_chart(sensor_distributions(raw_df), use_container_width=True)
    with right:
        st.plotly_chart(maintenance_breakdown(raw_df), use_container_width=True)

    st.plotly_chart(rul_distribution(raw_df), use_container_width=True)


# ======================================================================
#  PREDICT
# ======================================================================
elif page == "Predict":

    st.header("Run a Prediction")
    st.caption("Enter the current sensor readings and operational hours for a machine.")

    # inputs in a 2x2 grid so they don't stack into a tall column
    col1, col2 = st.columns(2)
    with col1:
        sensor_1 = st.number_input("Sensor 1", value=0.0, step=0.1, format="%.2f")
        sensor_3 = st.number_input("Sensor 3", value=0.0, step=0.1, format="%.2f")
    with col2:
        sensor_2 = st.number_input("Sensor 2", value=0.0, step=0.1, format="%.2f")
        operational_hours = st.number_input(
            "Operational Hours", min_value=0, max_value=10000, value=1000, step=50,
        )

    run = st.button("Run Prediction")

    if run:
        st.divider()

        # edge case: machine already past its rated life
        if operational_hours >= 10000:
            st.error("Machine has exceeded rated operational hours - "
                     "**immediate inspection required.**")
            st.metric("Maintenance Level", "Critical", delta="Overdue",
                      delta_color="inverse")
        else:
            rul, maintenance, cluster = predict(
                scaler, rul_model, maint_model, anomaly_model,
                sensor_1, sensor_2, sensor_3, operational_hours,
            )

            # severity banner
            if operational_hours >= 7000:
                st.warning("High operational usage - machine is approaching limits.")
                level = "Medium"
            else:
                st.success("Machine is within safe operating range.")
                level = "Normal"

            # metric cards
            m1, m2, m3 = st.columns(3)
            m1.metric("Remaining Life", f"{rul:,.0f} hrs")
            m2.metric("Maintenance", "Required" if maintenance else "Not Required")
            m3.metric("Anomaly", "Detected" if cluster == 1 else "None")

            # gauge visualisation
            left, right = st.columns([1.2, 1])
            with left:
                st.plotly_chart(rul_gauge(rul), use_container_width=True)
            with right:
                st.plotly_chart(
                    feature_importance(rul_model, FEATURE_COLS),
                    use_container_width=True,
                )


# ======================================================================
#  EXPLORE DATA
# ======================================================================
elif page == "Explore Data":

    st.header("Explore the Dataset")

    tab_viz, tab_raw = st.tabs(["Visualizations", "Raw Data"])

    with tab_viz:
        left, right = st.columns(2)
        with left:
            st.plotly_chart(correlation_heatmap(raw_df), use_container_width=True)
        with right:
            st.plotly_chart(
                feature_importance(rul_model, FEATURE_COLS),
                use_container_width=True,
            )
        st.plotly_chart(hours_vs_rul(raw_df), use_container_width=True)

    with tab_raw:
        st.caption(f"Showing the first 100 rows out of {len(raw_df):,}.")
        # let the user toggle maintenance-only view
        only_maint = st.checkbox("Show only records flagged for maintenance")
        display_df = pd.read_csv("machinery_data.csv")
        if only_maint:
            display_df = display_df[display_df["maintenance"] == 1]
        st.dataframe(display_df.head(100), use_container_width=True)


# ======================================================================
#  ABOUT
# ======================================================================
elif page == "About":

    st.header("About This Project")

    st.markdown("""
    This dashboard was built as part of a predictive maintenance research
    project at **MIT World Peace University, Pune**.  It combines three
    machine-learning approaches to assess industrial machinery health:

    | Model | Purpose |
    |---|---|
    | **Gradient Boosting Regressor** | Estimate Remaining Useful Life (RUL) |
    | **Gradient Boosting Classifier** | Flag whether maintenance is needed |
    | **K-Means Clustering** | Detect anomalous operating patterns |

    The models are trained on historical sensor data (vibration, temperature,
    and pressure proxies) along with cumulative operational hours.
    """)

    st.divider()

    st.subheader("Team - Panel A")
    team = st.columns(4)
    names = [
        "Shreyas Kshirsagar",
        "Ashlesha Chikhale",
        "Sudhanshu Athanimath",
        "Rutuja Dere",
    ]
    emails = [
        "1032220380@mitwpu.edu.in",
        "1032220257@mitwpu.edu.in",
        "1032220455@mitwpu.edu.in",
        "1032220258@mitwpu.edu.in",
    ]
    for col, name, email in zip(team, names, emails):
        with col:
            st.markdown(f"""
            <div class="stat-card" style="padding:1rem;">
                <p style="margin:0; font-size:1rem; font-weight:bold; color:#feca57;">{name}</p>
                <p style="font-size:0.8rem; word-break:break-all; margin-top:0.5rem; color:#bdc3c7;">{email}</p>
            </div>
            """, unsafe_allow_html=True)
