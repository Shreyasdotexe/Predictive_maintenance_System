"""
Custom CSS for the Streamlit app.  Kept in one place so `app.py` stays
clean and the theme is easy to tweak.
"""

import streamlit as st


def inject_css():
    """Inject the custom stylesheet into the Streamlit page."""
    st.markdown(_CSS, unsafe_allow_html=True)


_CSS = """
<style>
    /* --- base --------------------------------------------------- */
    .stApp {
        background: linear-gradient(160deg, #1a1a2e 0%, #16213e 40%, #0f3460 100%);
        color: #ecf0f1;
    }

    .block-container {
        padding: 2rem 2.5rem;
        max-width: 1100px;
    }

    h1, h2, h3, h4 { color: #ecf0f1; }

    /* --- sidebar ------------------------------------------------- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f3460 0%, #1a1a2e 100%);
    }
    section[data-testid="stSidebar"] .stRadio label {
        color: #ecf0f1 !important;
    }

    /* --- hero card (home page) ----------------------------------- */
    .hero-card {
        background: linear-gradient(135deg, #0f3460 0%, #533483 100%);
        padding: 3rem 2rem;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
        border: 1px solid rgba(255, 255, 255, 0.06);
    }
    .hero-card h1 {
        font-size: 2.4rem;
        color: #feca57;
        margin-bottom: 0.3rem;
    }
    .hero-card p {
        color: #bdc3c7;
        font-size: 1.1rem;
    }

    /* --- stat cards row ------------------------------------------ */
    .stat-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(6px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1.2rem 1rem;
        text-align: center;
    }
    .stat-card h2 {
        color: #feca57;
        margin: 0;
        font-size: 2rem;
    }
    .stat-card p {
        color: #bdc3c7;
        margin: 0.3rem 0 0;
        font-size: 0.9rem;
    }

    /* --- prediction result card ---------------------------------- */
    .result-card {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1rem;
    }

    /* --- contact section ----------------------------------------- */
    .contact-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 2rem;
    }

    /* --- buttons ------------------------------------------------- */
    .stButton > button {
        background: linear-gradient(135deg, #0f3460, #533483);
        color: #feca57;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(83, 52, 131, 0.4);
    }

    /* --- divider ------------------------------------------------- */
    hr { border-color: rgba(255, 255, 255, 0.08); }

    /* --- tabs ---------------------------------------------------- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }
    .stTabs [data-baseweb="tab"] {
        color: #bdc3c7;
    }
    .stTabs [aria-selected="true"] {
        color: #feca57 !important;
        border-bottom-color: #feca57 !important;
    }
</style>
"""
