"""
╔══════════════════════════════════════════════════════════════════╗
║  CONFIG.PY ▸ System Constants & Aesthetic Configuration        ║
║  All tunable parameters, column definitions, and CSS live here ║
╚══════════════════════════════════════════════════════════════════╝
"""

# ═══════════════════════════════════════════════════════════════════
# DATA PATHS
# ═══════════════════════════════════════════════════════════════════

DATA_PATH = "milk_combined_full_dataset.csv"

# ═══════════════════════════════════════════════════════════════════
# COLUMN DEFINITIONS — LEAKAGE & IDENTITY SAFETY
# ═══════════════════════════════════════════════════════════════════

# Columns that MUST be dropped to prevent data leakage
LEAKAGE_COLS = [
    "Quality_Score_0_100",
    "FSSAI_Compliance",
    "Adulterant_Detected",
    "Adulteration_Index_0_1",
    "FSSAI_Chemical_Score",
]

# Non-feature identity/categorical columns
ID_COLS = [
    "Sample_ID",
    "Company_Name",
    "Brand_Name",
    "Organization_Type",
    "State",
    "Market_Tier",
    "Market_Segment",
    "Collection_Date",
    "Season",
    "Collection_Point",
    "Milk_Type",
]

TARGET_COL = "Is_Adulterated"

# ═══════════════════════════════════════════════════════════════════
# PHYSICAL / CHEMICAL PARAMETERS FOR EDA SELECTORS
# ═══════════════════════════════════════════════════════════════════

PHYSICAL_PARAMS = [
    "Fat_percent",
    "SNF_percent",
    "Protein_percent",
    "Lactose_percent",
    "pH",
    "Specific_Gravity",
    "Acidity_Titratable_pct",
    "Viscosity_cP",
    "Freezing_Point_C",
    "Conductivity_mS_cm",
    "CLR_Corrected_Lactometer",
    "Urea_mg_per_100mL",
    "Melamine_ppm",
    "Estimated_Added_Water_pct",
    "Chloride_mg_per_100mL",
    "Casein_Whey_Ratio",
    "Refractive_Index",
]

# ═══════════════════════════════════════════════════════════════════
# ML PIPELINE HYPER-PARAMETERS
# ═══════════════════════════════════════════════════════════════════

TEST_SIZE = 0.2
RANDOM_STATE = 42
MAX_ITER = 2000
SOLVER = "lbfgs"
REGULARIZATION_C = 1.0

# ═══════════════════════════════════════════════════════════════════
# COLOR PALETTE — CYBER-INDUSTRIAL AESTHETIC
# ═══════════════════════════════════════════════════════════════════

COLORS = {
    "bg_primary": "#0d1117",
    "bg_secondary": "#161b22",
    "bg_tertiary": "#1c2333",
    "border": "#30363d",
    "neon_green": "#00ff41",
    "neon_green_dim": "#00cc33",
    "neon_green_glow": "rgba(0, 255, 65, 0.15)",
    "neon_red": "#ff003c",
    "neon_red_dim": "#cc0030",
    "neon_red_glow": "rgba(255, 0, 60, 0.15)",
    "neon_cyan": "#00e5ff",
    "neon_amber": "#ffab00",
    "text_primary": "#e6edf3",
    "text_secondary": "#8b949e",
    "text_muted": "#484f58",
}

# ═══════════════════════════════════════════════════════════════════
# MATPLOTLIB DARK THEME PARAMS
# ═══════════════════════════════════════════════════════════════════

MPL_DARK_PARAMS = {
    "figure.facecolor": COLORS["bg_primary"],
    "axes.facecolor": COLORS["bg_secondary"],
    "axes.edgecolor": COLORS["border"],
    "axes.labelcolor": COLORS["text_secondary"],
    "axes.grid": True,
    "grid.color": COLORS["border"],
    "grid.alpha": 0.5,
    "grid.linewidth": 0.5,
    "xtick.color": COLORS["text_secondary"],
    "ytick.color": COLORS["text_secondary"],
    "text.color": COLORS["text_primary"],
    "font.family": "monospace",
    "font.size": 9,
    "legend.facecolor": COLORS["bg_secondary"],
    "legend.edgecolor": COLORS["border"],
    "legend.fontsize": 8,
}

# ═══════════════════════════════════════════════════════════════════
# GLOBAL CSS INJECTION — CYBER-INDUSTRIAL THEME
# ═══════════════════════════════════════════════════════════════════

CYBER_CSS = """
<style>
    /* ── Import monospace font ── */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

    /* ── Root variables ── */
    :root {
        --bg-primary: #0d1117;
        --bg-secondary: #161b22;
        --bg-tertiary: #1c2333;
        --border-color: #30363d;
        --neon-green: #00ff41;
        --neon-green-dim: #00cc33;
        --neon-green-glow: rgba(0, 255, 65, 0.15);
        --neon-red: #ff003c;
        --neon-red-dim: #cc0030;
        --neon-red-glow: rgba(255, 0, 60, 0.15);
        --neon-cyan: #00e5ff;
        --neon-amber: #ffab00;
        --text-primary: #e6edf3;
        --text-secondary: #8b949e;
        --text-muted: #484f58;
    }

    /* ── Global overrides ── */
    .stApp, .main, [data-testid="stAppViewContainer"] {
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        font-family: 'JetBrains Mono', 'Courier New', monospace !important;
    }

    [data-testid="stHeader"] {
        background-color: var(--bg-primary) !important;
        border-bottom: 1px solid var(--border-color) !important;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background-color: var(--bg-secondary) !important;
        border-right: 1px solid var(--neon-green) !important;
        box-shadow: 2px 0 15px var(--neon-green-glow) !important;
    }

    [data-testid="stSidebar"] * {
        font-family: 'JetBrains Mono', monospace !important;
        color: var(--text-primary) !important;
    }

    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stRadio label {
        color: var(--neon-green) !important;
        text-transform: uppercase !important;
        font-size: 0.75rem !important;
        letter-spacing: 2px !important;
    }

    /* ── Markdown text ── */
    .stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown span {
        font-family: 'JetBrains Mono', monospace !important;
        color: var(--text-primary) !important;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Share Tech Mono', 'JetBrains Mono', monospace !important;
        color: var(--neon-green) !important;
        text-transform: uppercase !important;
        letter-spacing: 3px !important;
        border-bottom: 1px solid var(--border-color) !important;
        padding-bottom: 8px !important;
    }

    /* ── Metrics ── */
    [data-testid="stMetricValue"] {
        font-family: 'Share Tech Mono', monospace !important;
        color: var(--neon-green) !important;
        font-size: 1.8rem !important;
        text-shadow: 0 0 10px var(--neon-green-glow) !important;
    }

    [data-testid="stMetricLabel"] {
        font-family: 'JetBrains Mono', monospace !important;
        color: var(--text-secondary) !important;
        text-transform: uppercase !important;
        font-size: 0.7rem !important;
        letter-spacing: 2px !important;
    }

    /* ── Dataframes ── */
    [data-testid="stDataFrame"], .stDataFrame {
        border: 1px solid var(--border-color) !important;
        border-radius: 0px !important;
    }

    /* ── Selectbox / Input widgets ── */
    .stSelectbox > div > div,
    .stTextInput > div > div,
    .stNumberInput > div > div {
        background-color: var(--bg-tertiary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 0px !important;
        color: var(--text-primary) !important;
        font-family: 'JetBrains Mono', monospace !important;
    }

    .stSelectbox > div > div:focus-within,
    .stTextInput > div > div:focus-within {
        border-color: var(--neon-green) !important;
        box-shadow: 0 0 8px var(--neon-green-glow) !important;
    }

    /* ── Buttons ── */
    .stButton > button {
        background-color: transparent !important;
        border: 1px solid var(--neon-green) !important;
        color: var(--neon-green) !important;
        border-radius: 0px !important;
        font-family: 'JetBrains Mono', monospace !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        background-color: var(--neon-green) !important;
        color: var(--bg-primary) !important;
        box-shadow: 0 0 20px var(--neon-green-glow) !important;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px !important;
        border-bottom: 1px solid var(--border-color) !important;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: var(--bg-secondary) !important;
        color: var(--text-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-bottom: none !important;
        border-radius: 0px !important;
        font-family: 'JetBrains Mono', monospace !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        font-size: 0.75rem !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: var(--bg-tertiary) !important;
        color: var(--neon-green) !important;
        border-top: 2px solid var(--neon-green) !important;
    }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        background-color: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 0px !important;
        color: var(--neon-green) !important;
        font-family: 'JetBrains Mono', monospace !important;
        text-transform: uppercase !important;
    }

    /* ── Dividers ── */
    hr {
        border-color: var(--border-color) !important;
    }

    /* ── Radio buttons ── */
    .stRadio > div {
        background-color: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        padding: 10px !important;
        border-radius: 0px !important;
    }

    .stRadio [data-testid="stMarkdownContainer"] p {
        font-size: 0.8rem !important;
        letter-spacing: 1px !important;
    }

    /* ── Alert boxes ── */
    .stAlert {
        border-radius: 0px !important;
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: var(--bg-primary);
    }
    ::-webkit-scrollbar-thumb {
        background: var(--border-color);
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--neon-green-dim);
    }

    /* ── Spinner ── */
    .stSpinner > div > div {
        border-top-color: var(--neon-green) !important;
    }

    /* ── Plotly/Matplotlib container ── */
    [data-testid="stImage"] {
        border: 1px solid var(--border-color) !important;
        padding: 4px !important;
        border-radius: 0px !important;
    }

    /* ── Block container padding ── */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }

    /* ── Animated scan line (top bar) ── */
    @keyframes scanline {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }

    .scanline-bar {
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--neon-green), transparent);
        animation: scanline 3s linear infinite;
        margin-bottom: 1rem;
    }

    /* ── Glitch text effect for headers ── */
    @keyframes flicker {
        0%, 19.999%, 22%, 62.999%, 64%, 64.999%, 70%, 100% {
            opacity: 1;
        }
        20%, 21.999%, 63%, 63.999%, 65%, 69.999% {
            opacity: 0.4;
        }
    }
</style>
"""
