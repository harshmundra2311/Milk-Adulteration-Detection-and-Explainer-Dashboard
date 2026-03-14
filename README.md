# 🧪 MILK-DIAG — Physico-Chemical Adulteration Classifier

> An interactive, machine-learning-powered Streamlit dashboard that detects milk adulteration and explains the chemical reasoning behind its predictions using SHAP force diagnostics.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.55-FF4B4B?logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.8-F7931E?logo=scikit-learn&logoColor=white)
![SHAP](https://img.shields.io/badge/SHAP-0.51-purple)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📋 Overview

**MILK-DIAG** is a cyber-industrial diagnostic dashboard that classifies milk samples as **Pure** or **Adulterated** based on 94 physico-chemical parameters. It goes beyond simple prediction by providing transparent, explainable AI diagnostics through SHAP (SHapley Additive exPlanations), showing exactly which chemical features drove each decision.

### Key Features

- **🔍 Raw Data Inspection** — Explore the dataset with system-level metrics, class distribution charts, and feature statistics
- **🧬 Chemical Feature Isolation (EDA)** — Interactive scatter plots, correlation heatmaps, and distribution comparisons between pure and adulterated samples
- **⚙️ Algorithm Deployment & SHAP Diagnostics** — Run live sample-level predictions with full SHAP force breakdown explaining which features (e.g., high pH, low specific gravity) influenced the verdict

---

## 🖥️ Screenshots

| Raw Data Inspection | Chemical Feature EDA | SHAP Force Breakdown |
|---|---|---|
| KPI metrics, class balance chart, feature stats | Scatter plots, correlation matrix, KDE overlays | Verdict box, SHAP bar chart, force plot |

---

## 🏗️ Architecture

```
milk-diag/
├── app.py                     # Main entry point — slim orchestrator
├── config.py                  # Constants, column lists, colors, CSS, ML params
├── data_engine.py             # Cached data loading, cleaning, ML training pipeline
├── ui_components.py           # Reusable UI renderers (header, metrics, verdict, sidebar)
├── modules/
│   ├── __init__.py
│   ├── raw_data.py            # Module 1: Raw Data Inspection
│   ├── eda.py                 # Module 2: Chemical Feature Isolation (EDA)
│   └── shap_diagnostics.py    # Module 3: Algorithm Deployment & SHAP Diagnostics
├── milk_combined_full_dataset.csv   # Dataset (not tracked in git)
├── requirements.txt
├── .gitignore
└── README.md
```

### Module Responsibilities

| Module | Purpose |
|---|---|
| `config.py` | All tunable constants — colors, column definitions, CSS, hyperparameters |
| `data_engine.py` | Cached data loading, META/leakage column stripping, `LogisticRegression` training |
| `ui_components.py` | Shared HTML/CSS renderers — system header, metric cards, verdict box, sidebar, footer |
| `modules/raw_data.py` | KPI metrics, class distribution chart, descriptive statistics, dataframe preview |
| `modules/eda.py` | Interactive scatter plots, correlation heatmap, histogram + KDE distribution overlay |
| `modules/shap_diagnostics.py` | Model metrics, confusion matrix, sample-level SHAP bar chart, force plot, ranked table |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- The dataset file `milk_combined_full_dataset.csv` placed in the project root

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/milk-diag.git
cd milk-diag

# Install dependencies
pip install -r requirements.txt
```

### Running the Dashboard

```bash
streamlit run app.py
```

The app will open at [http://localhost:8501](http://localhost:8501).

---

## 🧠 ML Pipeline

| Component | Implementation |
|---|---|
| **Algorithm** | Logistic Regression (`sklearn.linear_model.LogisticRegression`) |
| **Scaling** | StandardScaler (zero mean, unit variance) |
| **Imbalance Handling** | `class_weight='balanced'` — adjusts penalty inversely proportional to class frequency |
| **Train/Test Split** | 80/20, stratified by target, `random_state=42` |
| **Explainability** | SHAP `LinearExplainer` for per-feature contribution analysis |

### Data Leakage Prevention

The following columns are **explicitly dropped** before training to prevent information leakage:

- `Quality_Score_0_100` — derived from target
- `FSSAI_Compliance` — derived from target
- `Adulterant_Detected` — contains target information
- `Adulteration_Index_0_1` — derived from target
- `FSSAI_Chemical_Score` — derived from target
- All `__META_` suffix columns (396 reference metadata columns)

---

## 📊 Dataset

- **Source**: Indian Milk Adulteration Detection Dataset (synthetic, educational)
- **Samples**: 2,500 (2,376 pure / 124 adulterated — ~95%/5% split)
- **Raw Columns**: 524 (128 features + 396 reference metadata)
- **Active Features**: 94 numeric parameters after cleaning
- **Adulterant Types**: 11 (Water, Urea, Detergent, Starch, Formalin, H₂O₂, SMP, Glucose, NaHCO₃, Vegetable Oil, Melamine)

> ⚠️ This is a **100% synthetically generated** dataset for educational and ML research purposes only.

---

## 🎨 Design Philosophy

The UI follows a strict **cyber-industrial** aesthetic inspired by factory diagnostic terminals:

- **Backgrounds**: Deep dark tones (`#0d1117`, `#161b22`)
- **Accents**: Neon green (`#00ff41`) for success/headers, neon red (`#ff003c`) for alerts
- **Typography**: JetBrains Mono + Share Tech Mono — monospace throughout
- **Styling**: Sharp edges (zero border-radius), terminal-style uppercase text, visible gridlines
- **Animations**: Scanline bar, hover transitions on buttons

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| ML | scikit-learn (LogisticRegression, StandardScaler) |
| Explainability | SHAP (LinearExplainer) |
| Visualization | Matplotlib, Seaborn |
| Data | Pandas, NumPy |

---

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgements

- Dataset generated using FSSAI/BIS chemical standards and domain-based simulation
- SHAP library by Scott Lundberg for model interpretability
- Streamlit for rapid dashboard prototyping
