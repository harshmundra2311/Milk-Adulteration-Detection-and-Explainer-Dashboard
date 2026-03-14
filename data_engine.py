"""
╔══════════════════════════════════════════════════════════════════╗
║  DATA_ENGINE.PY ▸ Cached Data Loading & ML Pipeline            ║
║  Handles ingestion, cleaning, training, and metric generation  ║
╚══════════════════════════════════════════════════════════════════╝
"""

import pandas as pd
import numpy as np
import streamlit as st

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    f1_score,
    precision_score,
    recall_score,
    accuracy_score,
)

from config import (
    DATA_PATH,
    LEAKAGE_COLS,
    ID_COLS,
    TARGET_COL,
    TEST_SIZE,
    RANDOM_STATE,
    MAX_ITER,
    SOLVER,
    REGULARIZATION_C,
)


# ═══════════════════════════════════════════════════════════════════
# DATA LOADING
# ═══════════════════════════════════════════════════════════════════


@st.cache_data(show_spinner=False)
def load_raw_data():
    """▸ DATA_LOADER :: Ingest raw CSV into memory."""
    df = pd.read_csv(DATA_PATH)
    return df


# ═══════════════════════════════════════════════════════════════════
# FEATURE EXTRACTION & CLEANING
# ═══════════════════════════════════════════════════════════════════


@st.cache_data(show_spinner=False)
def get_clean_features(df):
    """
    ▸ FEATURE_EXTRACTOR :: Strip META, leakage, and ID columns.
    Returns:
        df_clean: DataFrame with only usable columns
        feature_cols: list of numeric feature column names
    """
    # Remove META columns
    cols = [c for c in df.columns if "__META_" not in c]
    df_clean = df[cols].copy()

    # Drop leakage columns
    drop = [c for c in LEAKAGE_COLS if c in df_clean.columns]
    df_clean = df_clean.drop(columns=drop)

    # Separate features from target/identity
    feature_cols = [
        c
        for c in df_clean.select_dtypes(include="number").columns
        if c != TARGET_COL and c not in ID_COLS
    ]

    return df_clean, feature_cols


# ═══════════════════════════════════════════════════════════════════
# ML TRAINING PIPELINE
# ═══════════════════════════════════════════════════════════════════


@st.cache_resource(show_spinner=False)
def train_pipeline(_df_clean, feature_cols):
    """
    ▸ ML_ENGINE :: Train Logistic Regression with StandardScaler.
    Handles class imbalance via class_weight='balanced'.

    Returns:
        model:            Fitted LogisticRegression
        scaler:           Fitted StandardScaler
        X_test:           Unscaled test features (DataFrame)
        y_test:           Test labels (Series)
        idx_test:         Original DataFrame indices for test set
        feature_names:    List of feature column names
        metrics:          Dict of evaluation metrics
        X_train_scaled:   Scaled training data (for SHAP background)
    """
    X = _df_clean[feature_cols].copy()
    y = _df_clean[TARGET_COL].copy()

    # Handle any remaining NaN by filling with column median
    X = X.fillna(X.median())

    X_train, X_test, y_train, y_test, idx_train, idx_test = train_test_split(
        X, y, X.index, test_size=TEST_SIZE, stratify=y, random_state=RANDOM_STATE
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = LogisticRegression(
        class_weight="balanced",
        max_iter=MAX_ITER,
        solver=SOLVER,
        random_state=RANDOM_STATE,
        C=REGULARIZATION_C,
    )
    model.fit(X_train_scaled, y_train)

    # Generate predictions and metrics
    y_pred = model.predict(X_test_scaled)
    y_proba = model.predict_proba(X_test_scaled)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, y_proba),
        "confusion_matrix": confusion_matrix(y_test, y_pred),
        "classification_report": classification_report(
            y_test, y_pred, target_names=["PURE", "ADULTERATED"]
        ),
    }

    return (
        model,
        scaler,
        X_test,
        y_test,
        idx_test,
        feature_cols,
        metrics,
        X_train_scaled,
    )
