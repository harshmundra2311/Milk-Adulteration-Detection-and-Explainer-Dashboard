"""
╔══════════════════════════════════════════════════════════════════╗
║  UI_COMPONENTS.PY ▸ Reusable Visual Rendering Functions        ║
║  All shared HTML/CSS renderers for the diagnostic interface    ║
╚══════════════════════════════════════════════════════════════════╝
"""

import streamlit as st


# ═══════════════════════════════════════════════════════════════════
# SYSTEM HEADER
# ═══════════════════════════════════════════════════════════════════


def render_system_header():
    """Render the main system header with animated scanline."""
    st.markdown(
        """
        <div style="
            border: 1px solid #30363d;
            padding: 20px 30px;
            margin-bottom: 1.5rem;
            background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #1c2333 100%);
            position: relative;
            overflow: hidden;
        ">
            <div style="
                position: absolute; top: 0; left: 0; right: 0;
                height: 2px;
                background: linear-gradient(90deg, transparent, #00ff41, transparent);
                animation: scanline 2s linear infinite;
            "></div>
            <p style="
                font-family: 'Share Tech Mono', monospace;
                color: #00ff41;
                font-size: 0.65rem;
                letter-spacing: 4px;
                margin-bottom: 4px;
                text-transform: uppercase;
            ">▸ SYSTEM ONLINE ▸ DIAGNOSTIC ENGINE ACTIVE</p>
            <h1 style="
                font-family: 'Share Tech Mono', monospace;
                color: #00ff41;
                font-size: 1.8rem;
                margin: 0;
                letter-spacing: 5px;
                text-shadow: 0 0 20px rgba(0,255,65,0.3);
                border: none !important;
                padding-bottom: 0 !important;
            ">🧪 MILK-DIAG CLASSIFIER</h1>
            <p style="
                font-family: 'JetBrains Mono', monospace;
                color: #8b949e;
                font-size: 0.7rem;
                letter-spacing: 2px;
                margin-top: 6px;
                margin-bottom: 0;
            ">PHYSICO-CHEMICAL ADULTERATION DETECTION ▸ SHAP FORCE DIAGNOSTICS ▸ v3.1.7</p>
        </div>
    """,
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════
# METRIC CARD
# ═══════════════════════════════════════════════════════════════════


def render_metric_card(label, value, color="#00ff41", icon="▸"):
    """Render a custom styled metric card with neon glow."""
    st.markdown(
        f"""
        <div style="
            border: 1px solid #30363d;
            padding: 14px 18px;
            background: #161b22;
            margin-bottom: 8px;
        ">
            <p style="
                font-family: 'JetBrains Mono', monospace;
                color: #8b949e;
                font-size: 0.65rem;
                letter-spacing: 2px;
                text-transform: uppercase;
                margin-bottom: 4px;
            ">{icon} {label}</p>
            <p style="
                font-family: 'Share Tech Mono', monospace;
                color: {color};
                font-size: 1.6rem;
                margin: 0;
                text-shadow: 0 0 15px {color}33;
            ">{value}</p>
        </div>
    """,
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════
# SECTION HEADER
# ═══════════════════════════════════════════════════════════════════


def render_section_header(title, subtitle=""):
    """Render a section divider with green accent border."""
    sub_html = (
        f"""<p style="
        font-family: 'JetBrains Mono', monospace;
        color: #8b949e; font-size: 0.7rem;
        letter-spacing: 1px; margin-top: 4px;
    ">{subtitle}</p>"""
        if subtitle
        else ""
    )
    st.markdown(
        f"""
        <div style="
            border-left: 3px solid #00ff41;
            padding: 10px 18px;
            margin: 1.5rem 0 1rem 0;
            background: linear-gradient(90deg, rgba(0,255,65,0.05), transparent);
        ">
            <h3 style="
                font-family: 'Share Tech Mono', monospace;
                color: #00ff41;
                font-size: 1rem;
                letter-spacing: 3px;
                margin: 0;
                border: none !important;
                padding-bottom: 0 !important;
            ">◈ {title}</h3>
            {sub_html}
        </div>
    """,
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════
# VERDICT BOX
# ═══════════════════════════════════════════════════════════════════


def render_verdict_box(is_adulterated, probability):
    """Render a large verdict display box — PURE or ADULTERATED."""
    if is_adulterated:
        verdict = "⛔ ADULTERATED"
        color = "#ff003c"
        glow = "rgba(255,0,60,0.2)"
        border = "#ff003c"
        desc = "CONTAMINANT SIGNATURE DETECTED IN SAMPLE MATRIX"
    else:
        verdict = "✅ PURE — COMPLIANT"
        color = "#00ff41"
        glow = "rgba(0,255,65,0.2)"
        border = "#00ff41"
        desc = "ALL PARAMETERS WITHIN FSSAI TOLERANCE RANGE"

    st.markdown(
        f"""
        <div style="
            border: 2px solid {border};
            padding: 30px;
            text-align: center;
            background: linear-gradient(135deg, #0d1117, #161b22);
            box-shadow: 0 0 30px {glow}, inset 0 0 30px {glow};
            margin: 1rem 0;
        ">
            <p style="
                font-family: 'Share Tech Mono', monospace;
                color: #8b949e;
                font-size: 0.7rem;
                letter-spacing: 3px;
                margin-bottom: 8px;
            ">▸ SYSTEM VERDICT ▸</p>
            <h2 style="
                font-family: 'Share Tech Mono', monospace;
                color: {color};
                font-size: 2.2rem;
                margin: 0;
                text-shadow: 0 0 25px {glow};
                letter-spacing: 5px;
                border: none !important;
                padding-bottom: 0 !important;
            ">{verdict}</h2>
            <p style="
                font-family: 'JetBrains Mono', monospace;
                color: #8b949e;
                font-size: 0.7rem;
                letter-spacing: 2px;
                margin-top: 10px;
                margin-bottom: 0;
            ">{desc}</p>
            <div style="
                margin-top: 15px;
                padding-top: 15px;
                border-top: 1px solid #30363d;
            ">
                <span style="
                    font-family: 'Share Tech Mono', monospace;
                    color: {color};
                    font-size: 1.4rem;
                    text-shadow: 0 0 15px {glow};
                ">PROBABILITY: {probability:.4f}</span>
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════


def render_sidebar():
    """
    Render the sidebar control panel and return the selected mode.
    Returns:
        mode (str): One of the three operating mode strings.
    """
    with st.sidebar:
        st.markdown(
            """
            <div style="
                border-bottom: 1px solid #30363d;
                padding-bottom: 15px;
                margin-bottom: 20px;
            ">
                <p style="
                    font-family: 'Share Tech Mono', monospace;
                    color: #00ff41;
                    font-size: 1rem;
                    letter-spacing: 3px;
                    text-shadow: 0 0 10px rgba(0,255,65,0.3);
                    margin-bottom: 2px;
                ">⬡ CONTROL PANEL</p>
                <p style="
                    font-family: 'JetBrains Mono', monospace;
                    color: #484f58;
                    font-size: 0.6rem;
                    letter-spacing: 2px;
                ">SYSTEM NAVIGATION & PARAMETERS</p>
            </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(
            '<p style="font-family: \'JetBrains Mono\', monospace; color: #8b949e; '
            "font-size: 0.65rem; letter-spacing: 2px; text-transform: uppercase; "
            'margin-bottom: 4px;">▸ OPERATING MODE</p>',
            unsafe_allow_html=True,
        )
        mode = st.radio(
            "SELECT_MODE",
            options=[
                "🔍 RAW DATA INSPECTION",
                "🧬 CHEMICAL FEATURE ISOLATION",
                "⚙️ ALGORITHM DEPLOYMENT & SHAP",
            ],
            label_visibility="collapsed",
        )

        st.markdown("---")

        # System status indicator
        st.markdown(
            """
            <div style="
                border: 1px solid #30363d;
                padding: 12px;
                margin-top: 10px;
                background: #0d1117;
            ">
                <p style="font-family: 'JetBrains Mono', monospace; color: #8b949e;
                   font-size: 0.6rem; letter-spacing: 2px; margin-bottom: 8px;">
                   SYSTEM STATUS</p>
                <p style="font-family: 'JetBrains Mono', monospace; color: #00ff41;
                   font-size: 0.7rem; margin: 2px 0;">● ENGINE ONLINE</p>
                <p style="font-family: 'JetBrains Mono', monospace; color: #00ff41;
                   font-size: 0.7rem; margin: 2px 0;">● ML PIPELINE READY</p>
                <p style="font-family: 'JetBrains Mono', monospace; color: #00ff41;
                   font-size: 0.7rem; margin: 2px 0;">● SHAP KERNEL LOADED</p>
                <p style="font-family: 'JetBrains Mono', monospace; color: #484f58;
                   font-size: 0.55rem; margin-top: 8px; letter-spacing: 1px;">
                   BUILD: 3.1.7 // STABLE</p>
            </div>
        """,
            unsafe_allow_html=True,
        )

    return mode


# ═══════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════


def render_footer():
    """Render the bottom-of-page system footer."""
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; padding: 20px 0;">
            <p style="font-family: 'JetBrains Mono', monospace; color: #484f58;
               font-size: 0.6rem; letter-spacing: 3px;">
               ◈ MILK-DIAG CLASSIFIER v3.1.7 ◈ PHYSICO-CHEMICAL ANALYSIS ENGINE ◈</p>
            <p style="font-family: 'JetBrains Mono', monospace; color: #30363d;
               font-size: 0.5rem; letter-spacing: 2px;">
               LOGISTIC REGRESSION + STANDARD SCALER + SHAP LINEAR EXPLAINER //
               CLASS_WEIGHT=BALANCED</p>
            <p style="font-family: 'JetBrains Mono', monospace; color: #30363d;
               font-size: 0.5rem; letter-spacing: 2px; margin-top: 4px;">
               DATASET: INDIAN MILK ADULTERATION DETECTION — SYNTHETIC BENCHMARK //
               2,500 SAMPLES</p>
        </div>
    """,
        unsafe_allow_html=True,
    )
