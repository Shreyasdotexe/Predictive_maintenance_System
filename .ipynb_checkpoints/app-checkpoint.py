import streamlit as st
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Set page config
st.set_page_config(page_title="🔧 Predictive Maintenance", layout="wide")

# 🔹 Load and preprocess data
data = pd.read_csv("machinery_data.csv")
data.fillna(method="ffill", inplace=True)

# 🔹 Feature engineering
data['sensor_avg'] = data[['sensor_1', 'sensor_2', 'sensor_3']].mean(axis=1)
data['sensor_diff'] = data['sensor_1'] - data['sensor_2']
features = ['sensor_1', 'sensor_2', 'sensor_3', 'operational_hours', 'sensor_avg', 'sensor_diff']

# 🔹 Scale and train
scaler = StandardScaler()
data[features] = scaler.fit_transform(data[features])

reg_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
reg_model.fit(data[features], data['RUL'])

clf_model = GradientBoostingClassifier(n_estimators=100, random_state=42)
clf_model.fit(data[features], data['maintenance'])

kmeans = KMeans(n_clusters=2, random_state=42)
kmeans.fit(data[features])

# 🔹 Sidebar Navigation
page = st.sidebar.selectbox("📂 Navigation", ["🏠 Home", "📈 Dashboard", "📊 Data", "📬 Contact"])

# 🔹 Custom CSS styling
st.markdown("""
    <style>
        /* Body Background Gradient */
        body {
            background: linear-gradient(120deg, #1f1c2c, #928dab);
        }
        .stApp {
            background-color: #3b5669;
            color: white;
        }
        .block-container {
            padding: 2rem;
        }
        h1, h2, h3, h4, h5, h6, .stMarkdown {
            color: #ffffff;
        }

        /* Sidebar styling */
        .css-1d391kg {  /* Sidebar container */
            background-color: #2c3e50 !important;  /* Dark blue/black for the sidebar */
            color: white !important;
        }

        .css-1d391kg .stSidebar {
            background-color: #2c3e50 !important;  /* Sidebar background */
        }

        .css-1d391kg .stSidebar button {
            color: white !important;  /* Sidebar button text color */
        }

        /* Title Card */
        .title-card {
            background-color: #2c2f4a;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.5);
        }

        .title-card h1 {
            font-size: 40px;
            color: #feca57;
        }

        .title-card h3 {
            color: #ffffff;
            margin-top: 10px;
        }

        .stButton>button {
            background-color: #333333;
            color: white;
            font-weight: bold;
            font-size: 16px;
            border-radius: 10px;
            padding: 10px 24px;
        }

        .stNumberInput input {
            background-color: #ffffff;
            color: #000;
            border-radius: 10px;
            padding: 10px;
        }

        /* Contact Card */
        .contact-card {
            background-color: #2c3e50;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
            color: white;
            text-align: left;
        }

        .contact-header {
            text-align: center;
            font-size: 36px;
            color: #feca57;
            margin-bottom: 30px;
        }

        .contact-details {
            font-size: 18px;
            line-height: 1.8;
        }

        .result-card {
            background-color: #ffffff;
            color: #000;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }

    </style>
""", unsafe_allow_html=True)

# 🔹 Home Page
if page == "🏠 Home":
    st.markdown("""
        <div class="title-card">
            <h1>🔧 Predictive Maintenance Dashboard</h1>
            <h3>Smart Failure Prediction and Anomaly Detection</h3>
        </div>
        <br>
    """, unsafe_allow_html=True)
    st.markdown("Welcome to the Predictive Maintenance Dashboard! This tool allows you to:")
    st.markdown("- 📈 Predict Remaining Useful Life (RUL)")
    st.markdown("- 🛠️ Detect maintenance needs")
    st.markdown("- ⚠️ Identify potential anomalies based on sensor data")
    st.markdown("Use the sidebar to explore different sections!")

# 🔹 Dashboard Page
elif page == "📈 Dashboard":
    # Add space before the subheader
    st.markdown("<br><br><br>", unsafe_allow_html=True)  # Adjust number of <br> as needed

    st.subheader("📥 Enter Machine Data")
    
    # Input fields in a vertical layout
    sensor_1 = st.number_input("🔌 Sensor 1", value=0.0, step=0.1)
    sensor_2 = st.number_input("🔌 Sensor 2", value=0.0, step=0.1)
    sensor_3 = st.number_input("🔌 Sensor 3", value=0.0, step=0.1)
    operational_hours = st.number_input("⏱️ Operational Hours", min_value=0, max_value=10000, value=1000)

    # Feature prep
    sensor_avg = (sensor_1 + sensor_2 + sensor_3) / 3
    sensor_diff = sensor_1 - sensor_2
    input_data = np.array([[sensor_1, sensor_2, sensor_3, operational_hours, sensor_avg, sensor_diff]])
    input_scaled = scaler.transform(input_data)

    if st.button(" Predict Now "):
        st.markdown("---")
        st.subheader("📊 Prediction Results")

        if operational_hours >= 10000:
            st.error("🚨 Machine is **OUT OF OPERATIONAL HOURS**!")
            st.markdown("🛠️ **Maintenance Recommendation:** 🔴 **Heavy Maintenance Required**")
        else:
            rul = reg_model.predict(input_scaled)[0]
            maintenance = clf_model.predict(input_scaled)[0]
            cluster = kmeans.predict(input_scaled)[0]

            if operational_hours >= 7000:
                st.warning("⚠️ High operational usage. Machine nearing limits.")
                st.markdown("🛠️ **Maintenance Recommendation:** 🟠 **Medium Maintenance Required**")
            else:
                st.info("✅ Machine is within safe operating range.")
                st.markdown("🛠️ **Maintenance Recommendation:** 🟢 **Normal Maintenance**")

            # Results in a bright white background card
            st.markdown("""
                <div class="result-card">
                    <h3>📊 Detailed Results</h3>
                    <p><b>⏳ Remaining Useful Life:</b> {:.2f} hrs</p>
                    <p><b>Maintenance Status:</b> {} </p>
                    <p><b>Anomaly Check:</b> {} </p>
                </div>
            """.format(rul, "🛠️ Needs Maintenance" if maintenance == 1 else "✅ Normal", "⚠️ Anomaly Detected" if cluster == 1 else "✅ No Anomaly"), unsafe_allow_html=True)

# ------------------- Data Viewer -------------------
elif page == "📊 Data":
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.title("📊 Historical Machinery Data")
    st.dataframe(pd.read_csv("machinery_data.csv").head(50))

# 🔹 Contact Page
elif page == "📬 Contact":
    st.markdown("""
        <div class="contact-card">
            <div class="contact-header">📬 Contact the Developer Team</div>
            <div class="contact-details">
                <b>Team:</b> Predictive Maintenance Panel A<br>
                <b>Emails:</b><br>
                📧 1032220257@mitwpu.edu.in<br>
                📧 1032220258@mitwpu.edu.in<br>
                📧 1032220380@mitwpu.edu.in<br>
                📧 1032220455@mitwpu.edu.in<br><br>
                <b>Project:</b> Predictive Maintenance using Machine Learning<br>
                <b>University:</b> MIT World Peace University, Pune<br>
            </div>
        </div>
    """, unsafe_allow_html=True)
