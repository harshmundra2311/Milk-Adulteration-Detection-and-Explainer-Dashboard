"""
╔══════════════════════════════════════════════════════════════════╗
║  MODULE 3 ▸ ALGORITHM DEPLOYMENT & SHAP DIAGNOSTICS            ║
║  Model metrics, confusion matrix, sample diagnostics, SHAP     ║
╚══════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
import shap

from config import TARGET_COL
from ui_components import render_metric_card, render_section_header, render_verdict_box


def render(df_clean, model, scaler, X_test, y_test, idx_test, feat_names, metrics, X_train_scaled):
    """
    Render the Algorithm Deployment & SHAP Diagnostics module.

    Args:
        df_clean:         Cleaned DataFrame (for Sample_ID lookup)
        model:            Fitted LogisticRegression
        scaler:           Fitted StandardScaler
        X_test:           Unscaled test features (DataFrame)
        y_test:           Test labels (Series)
        idx_test:         Original DataFrame indices for test set
        feat_names:       List of feature column names
        metrics:          Dict of evaluation metrics
        X_train_scaled:   Scaled training data (for SHAP background)
    """
    render_section_header(
        "ALGORITHM DEPLOYMENT & DIAGNOSTICS",
        "LOGISTIC REGRESSION ENGINE + SHAP CHEMICAL FORCE BREAKDOWN",
    )

    # ── Model Performance Metrics ──
    _render_performance_metrics(metrics)

    # ── Confusion Matrix & Classification Report ──
    _render_confusion_matrix(metrics)

    # ── Sample-Level Diagnostic ──
    _render_sample_diagnostic(
        df_clean, model, scaler, X_test, y_test, idx_test, feat_names, X_train_scaled
    )


# ═══════════════════════════════════════════════════════════════════
# PRIVATE RENDERERS
# ═══════════════════════════════════════════════════════════════════


def _render_performance_metrics(metrics):
    """Render the 5-column model performance KPI strip."""
    st.markdown(
        '<p style="font-family: \'JetBrains Mono\', monospace; color: #8b949e; '
        "font-size: 0.65rem; letter-spacing: 2px; text-transform: uppercase; "
        'margin-bottom: 8px;">▸ MODEL PERFORMANCE MATRIX</p>',
        unsafe_allow_html=True,
    )

    mc1, mc2, mc3, mc4, mc5 = st.columns(5)
    with mc1:
        render_metric_card("ACCURACY", f"{metrics['accuracy']:.4f}", "#00e5ff")
    with mc2:
        render_metric_card("F1 SCORE", f"{metrics['f1']:.4f}", "#00ff41")
    with mc3:
        render_metric_card("PRECISION", f"{metrics['precision']:.4f}", "#ffab00")
    with mc4:
        render_metric_card("RECALL", f"{metrics['recall']:.4f}", "#ff003c")
    with mc5:
        render_metric_card("ROC-AUC", f"{metrics['roc_auc']:.4f}", "#00ff41")


def _render_confusion_matrix(metrics):
    """Render confusion matrix heatmap + classification report."""
    render_section_header("CONFUSION MATRIX", "TRUE vs PREDICTED CLASSIFICATION GRID")

    fig, ax = plt.subplots(figsize=(6, 4.5))
    cm = metrics["confusion_matrix"]
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap=mcolors.LinearSegmentedColormap.from_list(
            "cm_cyber", ["#0d1117", "#00ff41"]
        ),
        xticklabels=["PURE", "ADULTERATED"],
        yticklabels=["PURE", "ADULTERATED"],
        linewidths=1,
        linecolor="#30363d",
        cbar=False,
        annot_kws={"size": 14, "fontweight": "bold", "fontfamily": "monospace"},
        ax=ax,
    )
    ax.set_xlabel("PREDICTED LABEL", fontsize=8, labelpad=10)
    ax.set_ylabel("TRUE LABEL", fontsize=8, labelpad=10)
    ax.set_title(
        "▸ CONFUSION MATRIX ▸ TEST SET",
        fontsize=9,
        pad=12,
        color="#00ff41",
    )
    ax.tick_params(labelsize=8)
    plt.tight_layout()

    col_cm, col_report = st.columns([1, 1])
    with col_cm:
        st.pyplot(fig)
    plt.close(fig)

    with col_report:
        st.markdown(
            '<p style="font-family: \'JetBrains Mono\', monospace; color: #8b949e; '
            "font-size: 0.65rem; letter-spacing: 2px; text-transform: uppercase; "
            'margin-bottom: 8px; margin-top: 1.5rem;">▸ CLASSIFICATION REPORT</p>',
            unsafe_allow_html=True,
        )
        st.code(metrics["classification_report"], language=None)


def _render_sample_diagnostic(
    df_clean, model, scaler, X_test, y_test, idx_test, feat_names, X_train_scaled
):
    """Render sample selector, verdict, feature readout, and SHAP plots."""
    render_section_header(
        "SAMPLE DIAGNOSTIC ENGINE",
        "SELECT A TEST SAMPLE FOR LIVE CLASSIFICATION & SHAP FORCE ANALYSIS",
    )

    # Build test sample lookup
    test_df = df_clean.loc[idx_test].copy()
    test_sample_ids = (
        test_df["Sample_ID"].values
        if "Sample_ID" in test_df.columns
        else idx_test.astype(str).values
    )

    st.markdown(
        '<p style="font-family: \'JetBrains Mono\', monospace; color: #8b949e; '
        "font-size: 0.65rem; letter-spacing: 2px; text-transform: uppercase; "
        'margin-bottom: 4px;">▸ SELECT SAMPLE ID FROM TEST DATASET</p>',
        unsafe_allow_html=True,
    )
    selected_sample = st.selectbox(
        "SAMPLE_ID",
        options=test_sample_ids,
        index=0,
        label_visibility="collapsed",
    )

    if not st.button("⚡ RUN DIAGNOSTIC", use_container_width=True):
        return

    with st.spinner("▸ EXECUTING DIAGNOSTIC PROTOCOL..."):
        # Resolve sample row
        if "Sample_ID" in test_df.columns:
            sample_row = test_df.loc[test_df["Sample_ID"] == selected_sample]
        else:
            sample_row = test_df.loc[[int(selected_sample)]]

        if sample_row.empty:
            st.error("▸ ERROR :: SAMPLE NOT FOUND IN TEST PARTITION")
            return

        sample_idx = sample_row.index[0]
        sample_features = X_test.loc[[sample_idx]]
        sample_features_filled = sample_features.fillna(X_test.median())
        sample_scaled = scaler.transform(sample_features_filled)

        true_label = y_test.loc[sample_idx]
        pred_proba = model.predict_proba(sample_scaled)[0][1]
        pred_label = int(pred_proba >= 0.5)

        # ── Verdict ──
        render_verdict_box(pred_label == 1, pred_proba)

        # ── Ground Truth Comparison ──
        gt_col1, gt_col2 = st.columns(2)
        with gt_col1:
            gt_text = "ADULTERATED" if true_label == 1 else "PURE"
            gt_color = "#ff003c" if true_label == 1 else "#00ff41"
            render_metric_card("GROUND TRUTH", gt_text, gt_color, "◉")
        with gt_col2:
            match = "MATCH ✓" if pred_label == true_label else "MISMATCH ✗"
            match_color = "#00ff41" if pred_label == true_label else "#ff003c"
            render_metric_card("PREDICTION vs TRUTH", match, match_color, "◎")

        # ── Sample Feature Values ──
        render_section_header(
            "SAMPLE FEATURE READOUT",
            f"RAW VALUES FOR SAMPLE {selected_sample}",
        )
        feature_readout = sample_features.T.copy()
        feature_readout.columns = ["VALUE"]
        feature_readout["VALUE"] = feature_readout["VALUE"].round(4)
        st.dataframe(feature_readout, use_container_width=True, height=300)

        # ── SHAP Analysis ──
        _render_shap_analysis(
            model,
            scaler,
            sample_scaled,
            sample_features_filled,
            feat_names,
            selected_sample,
            X_train_scaled,
        )


def _render_shap_analysis(
    model, scaler, sample_scaled, sample_features_filled, feat_names, sample_id, X_train_scaled
):
    """Compute SHAP values and render bar chart + force plot + table."""
    render_section_header(
        "CHEMICAL FORCE BREAKDOWN",
        "SHAP LINEAR EXPLAINER — FEATURE CONTRIBUTION TO CLASSIFICATION DECISION",
    )

    st.markdown(
        """<p style="font-family: 'JetBrains Mono', monospace; color: #8b949e;
        font-size: 0.7rem; letter-spacing: 1px; margin-bottom: 12px;">
        Each bar represents a chemical parameter's directional force on the model's output.
        <span style="color: #ff003c;">RED ▸</span> pushes toward ADULTERATED |
        <span style="color: #00ff41;">GREEN ▸</span> pushes toward PURE
        </p>""",
        unsafe_allow_html=True,
    )

    with st.spinner("▸ COMPUTING SHAP VALUES..."):
        # LinearExplainer for Logistic Regression
        explainer = shap.LinearExplainer(
            model, X_train_scaled, feature_names=feat_names
        )
        shap_values = explainer.shap_values(sample_scaled)
        shap_vals = shap_values[0] if len(shap_values.shape) > 1 else shap_values

        # ── Custom SHAP Bar Plot (top 20) ──
        _render_shap_bar_chart(feat_names, shap_vals, sample_id)

        # ── SHAP Force Plot (HTML) ──
        _render_shap_force_plot(
            explainer, shap_vals, sample_features_filled, feat_names
        )

        # ── Top Contributors Table ──
        _render_shap_table(feat_names, shap_vals)


def _render_shap_bar_chart(feat_names, shap_vals, sample_id):
    """Render horizontal bar chart of top 20 SHAP contributions."""
    feat_importance = pd.DataFrame(
        {"feature": feat_names, "shap_value": shap_vals}
    )
    feat_importance["abs_shap"] = feat_importance["shap_value"].abs()
    feat_importance = feat_importance.sort_values("abs_shap", ascending=True)

    top_n = feat_importance.tail(20)

    fig, ax = plt.subplots(figsize=(12, 8))
    colors = ["#ff003c" if v > 0 else "#00ff41" for v in top_n["shap_value"]]

    bars = ax.barh(
        range(len(top_n)),
        top_n["shap_value"].values,
        color=colors,
        edgecolor="#30363d",
        linewidth=0.5,
        height=0.7,
        alpha=0.85,
    )

    ax.set_yticks(range(len(top_n)))
    ax.set_yticklabels(
        [f.upper().replace("_", " ")[:35] for f in top_n["feature"]],
        fontsize=7,
    )

    ax.axvline(x=0, color="#8b949e", linewidth=0.8, linestyle="--")
    ax.set_xlabel(
        "SHAP VALUE (IMPACT ON MODEL OUTPUT)", fontsize=8, labelpad=10
    )
    ax.set_title(
        f"▸ CHEMICAL FORCE BREAKDOWN ▸ SAMPLE {sample_id}",
        fontsize=9,
        pad=12,
        color="#00ff41",
    )
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Value labels
    for i, (val, bar) in enumerate(zip(top_n["shap_value"].values, bars)):
        x_pos = val + (0.005 if val >= 0 else -0.005)
        ha = "left" if val >= 0 else "right"
        ax.text(
            x_pos,
            i,
            f"{val:+.4f}",
            va="center",
            ha=ha,
            fontsize=6,
            color="#e6edf3",
            fontfamily="monospace",
        )

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


def _render_shap_force_plot(explainer, shap_vals, sample_features_filled, feat_names):
    """Render interactive SHAP force plot as embedded HTML."""
    render_section_header(
        "SHAP FORCE PLOT",
        "INTERACTIVE FORCE VISUALIZATION — FEATURE PUSH/PULL DECOMPOSITION",
    )

    expected_value = explainer.expected_value
    if isinstance(expected_value, np.ndarray):
        expected_value = expected_value[0]

    force_plot = shap.force_plot(
        expected_value,
        shap_vals,
        sample_features_filled.values[0],
        feature_names=feat_names,
        matplotlib=False,
    )

    # Render as HTML within Streamlit using components
    shap_html = f"<head>{shap.getjs()}</head><body>{force_plot.html()}</body>"
    components.html(shap_html, height=180, scrolling=True)


def _render_shap_table(feat_names, shap_vals):
    """Render ranked top-15 feature contributions table."""
    render_section_header(
        "TOP FEATURE CONTRIBUTIONS",
        "RANKED CHEMICAL PARAMETERS BY ABSOLUTE SHAP IMPACT",
    )

    feat_importance = pd.DataFrame(
        {"feature": feat_names, "shap_value": shap_vals}
    )
    feat_importance["abs_shap"] = feat_importance["shap_value"].abs()

    top_table = (
        feat_importance.sort_values("abs_shap", ascending=False).head(15).copy()
    )
    top_table["DIRECTION"] = top_table["shap_value"].apply(
        lambda x: "→ ADULTERATED" if x > 0 else "→ PURE"
    )
    top_table["FEATURE"] = top_table["feature"].str.upper().str.replace("_", " ")
    top_table["SHAP VALUE"] = top_table["shap_value"].round(4)
    top_table["ABS IMPACT"] = top_table["abs_shap"].round(4)
    top_table["RANK"] = range(1, len(top_table) + 1)

    display_table = top_table[
        ["RANK", "FEATURE", "SHAP VALUE", "ABS IMPACT", "DIRECTION"]
    ].reset_index(drop=True)

    st.dataframe(display_table, use_container_width=True, hide_index=True)
