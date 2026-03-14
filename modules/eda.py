"""
╔══════════════════════════════════════════════════════════════════╗
║  MODULE 2 ▸ CHEMICAL FEATURE ISOLATION (EDA)                   ║
║  Interactive scatter plots, correlation heatmap, distributions  ║
╚══════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns

from config import TARGET_COL, PHYSICAL_PARAMS
from ui_components import render_section_header


def render(df_clean, feature_cols):
    """
    Render the Chemical Feature Isolation (EDA) module.

    Args:
        df_clean:      Cleaned DataFrame
        feature_cols:  List of active numeric feature column names
    """
    render_section_header(
        "CHEMICAL FEATURE ISOLATION",
        "INTERACTIVE SCATTER ANALYSIS — MAP PHYSICAL PARAMETERS & OBSERVE DECISION BOUNDARIES",
    )

    available_params = [p for p in PHYSICAL_PARAMS if p in feature_cols]

    # ── Axis Selectors ──
    col_x, col_y = st.columns(2)
    with col_x:
        st.markdown(
            '<p style="font-family: \'JetBrains Mono\', monospace; color: #8b949e; '
            "font-size: 0.65rem; letter-spacing: 2px; text-transform: uppercase;\">"
            "▸ X-AXIS PARAMETER</p>",
            unsafe_allow_html=True,
        )
        x_param = st.selectbox(
            "X_AXIS",
            options=available_params,
            index=0,
            label_visibility="collapsed",
        )
    with col_y:
        st.markdown(
            '<p style="font-family: \'JetBrains Mono\', monospace; color: #8b949e; '
            "font-size: 0.65rem; letter-spacing: 2px; text-transform: uppercase;\">"
            "▸ Y-AXIS PARAMETER</p>",
            unsafe_allow_html=True,
        )
        y_param = st.selectbox(
            "Y_AXIS",
            options=available_params,
            index=min(4, len(available_params) - 1),
            label_visibility="collapsed",
        )

    # ── Scatter Plot ──
    _render_scatter(df_clean, x_param, y_param)

    # ── Correlation Matrix ──
    _render_correlation(df_clean, available_params)

    # ── Distribution Comparison ──
    _render_distribution(df_clean, available_params)


# ═══════════════════════════════════════════════════════════════════
# PRIVATE RENDERERS
# ═══════════════════════════════════════════════════════════════════


def _render_scatter(df_clean, x_param, y_param):
    """Render pure vs. adulterated scatter plot."""
    fig, ax = plt.subplots(figsize=(12, 6))

    pure_mask = df_clean[TARGET_COL] == 0
    adult_mask = df_clean[TARGET_COL] == 1

    ax.scatter(
        df_clean.loc[pure_mask, x_param],
        df_clean.loc[pure_mask, y_param],
        c="#00ff41",
        alpha=0.35,
        s=18,
        label="PURE",
        edgecolors="#0d1117",
        linewidth=0.3,
        zorder=2,
    )
    ax.scatter(
        df_clean.loc[adult_mask, x_param],
        df_clean.loc[adult_mask, y_param],
        c="#ff003c",
        alpha=0.85,
        s=45,
        label="ADULTERATED",
        edgecolors="#ffffff",
        linewidth=0.6,
        marker="X",
        zorder=3,
    )

    ax.set_xlabel(x_param.upper().replace("_", " "), fontsize=8, labelpad=10)
    ax.set_ylabel(y_param.upper().replace("_", " "), fontsize=8, labelpad=10)
    ax.set_title(
        f"▸ CHEMICAL FEATURE SCATTER ▸ {x_param.upper()} vs {y_param.upper()}",
        fontsize=9,
        pad=12,
        color="#00ff41",
    )
    ax.legend(loc="upper right", fontsize=7, markerscale=0.8, framealpha=0.8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


def _render_correlation(df_clean, corr_features):
    """Render triangular correlation heatmap."""
    render_section_header(
        "CORRELATION MATRIX",
        "INTER-PARAMETER DEPENDENCY MAP — SELECTED PHYSICAL FEATURES",
    )

    corr_data = df_clean[corr_features].corr()

    fig, ax = plt.subplots(figsize=(12, 8))
    cmap = mcolors.LinearSegmentedColormap.from_list(
        "cyber", ["#ff003c", "#161b22", "#00ff41"]
    )
    mask = np.triu(np.ones_like(corr_data, dtype=bool), k=1)

    sns.heatmap(
        corr_data,
        mask=mask,
        cmap=cmap,
        vmin=-1,
        vmax=1,
        center=0,
        annot=True,
        fmt=".2f",
        annot_kws={"size": 6, "fontfamily": "monospace"},
        square=True,
        linewidths=0.5,
        linecolor="#30363d",
        cbar_kws={"shrink": 0.8, "label": "CORRELATION COEFFICIENT"},
        ax=ax,
    )
    ax.set_title(
        "▸ FEATURE CORRELATION HEATMAP",
        fontsize=9,
        pad=12,
        color="#00ff41",
    )
    ax.tick_params(axis="both", labelsize=6)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


def _render_distribution(df_clean, available_params):
    """Render histogram + KDE overlay for selected parameter."""
    render_section_header(
        "DISTRIBUTION COMPARISON",
        "KERNEL DENSITY OVERLAY — PURE vs ADULTERATED",
    )

    dist_param = st.selectbox(
        "SELECT PARAMETER FOR DISTRIBUTION ANALYSIS",
        options=available_params,
        index=0,
        key="dist_param",
    )

    fig, ax = plt.subplots(figsize=(12, 4))

    pure_vals = df_clean.loc[df_clean[TARGET_COL] == 0, dist_param].dropna()
    adult_vals = df_clean.loc[df_clean[TARGET_COL] == 1, dist_param].dropna()

    ax.hist(
        pure_vals,
        bins=50,
        alpha=0.3,
        color="#00ff41",
        label="PURE",
        density=True,
        edgecolor="#0d1117",
    )
    ax.hist(
        adult_vals,
        bins=30,
        alpha=0.5,
        color="#ff003c",
        label="ADULTERATED",
        density=True,
        edgecolor="#0d1117",
    )

    # KDE overlay
    if len(pure_vals) > 2:
        sns.kdeplot(
            pure_vals, color="#00ff41", linewidth=1.5, ax=ax, label="_nolegend_"
        )
    if len(adult_vals) > 2:
        sns.kdeplot(
            adult_vals, color="#ff003c", linewidth=1.5, ax=ax, label="_nolegend_"
        )

    ax.set_xlabel(dist_param.upper().replace("_", " "), fontsize=8, labelpad=10)
    ax.set_ylabel("DENSITY", fontsize=8, labelpad=10)
    ax.set_title(
        f"▸ DISTRIBUTION OVERLAY ▸ {dist_param.upper()}",
        fontsize=9,
        pad=12,
        color="#00ff41",
    )
    ax.legend(fontsize=7, loc="upper right")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
