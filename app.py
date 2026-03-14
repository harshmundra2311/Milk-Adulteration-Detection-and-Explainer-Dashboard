"""
╔══════════════════════════════════════════════════════════════════╗
║  APP.PY ▸ Main Entry Point — System Orchestrator               ║
║  Physico-Chemical Adulteration Classifier v3.1.7               ║
║  Industrial Diagnostic System — Milk Quality Analytics Engine  ║
╚══════════════════════════════════════════════════════════════════╝

Run:  streamlit run app.py
"""

import warnings
import streamlit as st
import matplotlib.pyplot as plt

from config import CYBER_CSS, MPL_DARK_PARAMS
from data_engine import load_raw_data, get_clean_features, train_pipeline
from ui_components import render_system_header, render_sidebar, render_footer
from modules import raw_data, eda, shap_diagnostics

warnings.filterwarnings("ignore")

# ═══════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="MILK-DIAG ▸ Adulteration Classifier",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════════
# INJECT GLOBAL CSS & APPLY MATPLOTLIB DARK THEME
# ═══════════════════════════════════════════════════════════════════

st.markdown(CYBER_CSS, unsafe_allow_html=True)
st.markdown('<div class="scanline-bar"></div>', unsafe_allow_html=True)
plt.rcParams.update(MPL_DARK_PARAMS)

# ═══════════════════════════════════════════════════════════════════
# SIDEBAR — OPERATING MODE SELECTOR
# ═══════════════════════════════════════════════════════════════════

mode = render_sidebar()

# ═══════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════

render_system_header()

# ═══════════════════════════════════════════════════════════════════
# DATA ENGINE INITIALIZATION
# ═══════════════════════════════════════════════════════════════════

with st.spinner("▸ INITIALIZING DATA ENGINE..."):
    df_raw = load_raw_data()
    df_clean, feature_cols = get_clean_features(df_raw)

with st.spinner("▸ TRAINING ML PIPELINE..."):
    model, scaler, X_test, y_test, idx_test, feat_names, metrics, X_train_scaled = (
        train_pipeline(df_clean, feature_cols)
    )

# ═══════════════════════════════════════════════════════════════════
# MODULE ROUTING
# ═══════════════════════════════════════════════════════════════════

if mode == "🔍 RAW DATA INSPECTION":
    raw_data.render(df_raw, df_clean, feature_cols)

elif mode == "🧬 CHEMICAL FEATURE ISOLATION":
    eda.render(df_clean, feature_cols)

elif mode == "⚙️ ALGORITHM DEPLOYMENT & SHAP":
    shap_diagnostics.render(
        df_clean, model, scaler, X_test, y_test,
        idx_test, feat_names, metrics, X_train_scaled,
    )

# ═══════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════

render_footer()
