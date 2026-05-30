# Predictive Maintenance Dashboard

A Streamlit-based dashboard that uses machine learning to predict equipment failures before they happen. Built with real sensor data and three complementary ML models.

## What It Does

- **Remaining Useful Life (RUL) estimation** - Gradient Boosting Regressor predicts how many operational hours a machine has left.
- **Maintenance flagging** - Gradient Boosting Classifier determines whether a machine needs maintenance based on current readings.
- **Anomaly detection** - K-Means clustering identifies unusual operating patterns that may indicate developing faults.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Visualizations | Plotly |
| ML Models | scikit-learn (Gradient Boosting, K-Means) |
| Data | pandas, NumPy |

## Project Structure

```
app.py                  # main Streamlit application
models.py               # data loading, feature engineering, model training
visualizations.py       # Plotly chart builders
styles.py               # custom CSS theme
machinery_data.csv      # historical sensor dataset (1000 records)
requirements.txt        # Python dependencies
.streamlit/
  config.toml           # Streamlit server & theme config
```

## Running Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`.

## Deployment

This project is deployed on [Streamlit Community Cloud](https://share.streamlit.io). 
You can view the live dashboard here: **[https://predictive-maintenance-dash-board.streamlit.app/](https://predictive-maintenance-dash-board.streamlit.app/)**

## Team

Panel A - MIT World Peace University, Pune
- Shreyas Kshirsagar (1032220380@mitwpu.edu.in)
- Ashlesha Chikhale (1032220257@mitwpu.edu.in)
- Sudhanshu Athanimath (1032220455@mitwpu.edu.in)
- Rutuja Dere (1032220258@mitwpu.edu.in)

