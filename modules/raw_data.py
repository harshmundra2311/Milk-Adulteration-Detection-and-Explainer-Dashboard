"""
╔══════════════════════════════════════════════════════════════════╗
║  MODULE 1 ▸ RAW DATA INSPECTION                               ║
║  Dataframe logs, system metrics, class distribution, stats     ║
╚══════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import matplotlib.pyplot as plt

from config import TARGET_COL, LEAKAGE_COLS
from ui_components import render_metric_card, render_section_header


def render(df_raw, df_clean, feature_cols):
    """
    Render the Raw Data Inspection module.

    Args:
        df_raw:        Original unprocessed DataFrame
        df_clean:      Cleaned DataFrame (META/leakage stripped)
        feature_cols:  List of active numeric feature column names
    """
    render_section_header(
        "RAW DATA INSPECTION",
        "PRIMARY DATAFRAME LOGS & HIGH-LEVEL SYSTEM METRICS",
    )

    # ── KPI Row 1 ──
    total_samples = len(df_raw)
    total_features_raw = df_raw.shape[1]
    active_features = len(feature_cols)
    meta_count = len([c for c in df_raw.columns if "__META_" in c])
    pure_count = int((df_clean[TARGET_COL] == 0).sum())
    adult_count = int((df_clean[TARGET_COL] == 1).sum())
    imbalance_ratio = pure_count / adult_count if adult_count > 0 else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_card("TOTAL SAMPLES", f"{total_samples:,}", "#00ff41", "◉")
    with c2:
        render_metric_card("ACTIVE FEATURES", f"{active_features}", "#00e5ff", "◎")
    with c3:
        render_metric_card("META DROPPED", f"{meta_count}", "#ffab00", "⊘")
    with c4:
        render_metric_card(
            "IMBALANCE RATIO", f"{imbalance_ratio:.1f}:1", "#ff003c", "⚠"
        )

    st.markdown("")

    # ── KPI Row 2 ──
    c5, c6, c7, c8 = st.columns(4)
    with c5:
        render_metric_card("PURE SAMPLES", f"{pure_count:,}", "#00ff41", "●")
    with c6:
        render_metric_card("ADULTERATED", f"{adult_count}", "#ff003c", "●")
    with c7:
        render_metric_card("RAW COLUMNS", f"{total_features_raw}", "#8b949e", "▦")
    with c8:
        render_metric_card("LEAKAGE COLS", f"{len(LEAKAGE_COLS)}", "#ffab00", "⊗")

    # ── Class Distribution Chart ──
    render_section_header("CLASS DISTRIBUTION", "TARGET VARIABLE FREQUENCY ANALYSIS")

    fig_dist, ax_dist = plt.subplots(figsize=(10, 3.5))
    counts = df_clean[TARGET_COL].value_counts().sort_index()
    bars = ax_dist.bar(
        ["PURE (0)", "ADULTERATED (1)"],
        counts.values,
        color=["#00ff41", "#ff003c"],
        edgecolor="#30363d",
        linewidth=1.5,
        width=0.5,
        alpha=0.85,
    )
    for bar, val in zip(bars, counts.values):
        ax_dist.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 20,
            f"{val:,}",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
            color="#e6edf3",
            fontfamily="monospace",
        )
    ax_dist.set_ylabel("FREQUENCY", fontsize=8, labelpad=10)
    ax_dist.set_title(
        "▸ TARGET CLASS BALANCE ▸ IS_ADULTERATED",
        fontsize=9,
        pad=12,
        color="#00ff41",
    )
    ax_dist.spines["top"].set_visible(False)
    ax_dist.spines["right"].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig_dist)
    plt.close(fig_dist)

    # ── Feature Statistics Table ──
    render_section_header(
        "FEATURE STATISTICS", "DESCRIPTIVE DIAGNOSTICS FOR ACTIVE VARIABLES"
    )

    stats_df = df_clean[feature_cols].describe().T
    stats_df = stats_df[["count", "mean", "std", "min", "25%", "50%", "75%", "max"]]
    stats_df = stats_df.round(4)
    stats_df.index.name = "FEATURE"

    st.dataframe(stats_df, use_container_width=True, height=450)

    # ── Raw Dataframe Preview ──
    render_section_header(
        "DATAFRAME LOG", "FIRST 100 RECORDS — CLEANED FEATURE MATRIX"
    )

    display_cols = ["Sample_ID"] + feature_cols[:15] + [TARGET_COL]
    display_cols = [c for c in display_cols if c in df_clean.columns]
    st.dataframe(df_clean[display_cols].head(100), use_container_width=True, height=400)
