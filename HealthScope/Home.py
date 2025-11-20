import streamlit as st
import pandas as pd
import numpy as np
import requests
from streamlit_lottie import st_lottie
from utils.layout import apply_custom_css, GradientHeader
from utils.themes import HealthScopeTheme as Theme
import json
from pathlib import Path

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(page_title="HealthScope", page_icon="🩺", layout="wide")
apply_custom_css()

# --------------------------------------------------
# THEME
# --------------------------------------------------
PRIMARY = Theme.HOME["primary"]
TEXT = Theme.HOME["text"]
GRADIENT = Theme.HOME["gradient"]

# Lottie loader (same fallback)
def load_lottie_url(url):
    try:
        r = requests.get(url, timeout=8, verify=False)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None

def load_lottie_file(path):
    try:
        p = Path(path)
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        pass
    return None

INLINE_FALLBACK = {
    "v": "5.7.4",
    "fr": 30,
    "ip": 0,
    "op": 90,
    "w": 300,
    "h": 300,
    "nm": "heartbeat",
    "ddd": 0,
    "assets": [],
    "layers": [
        {
            "ddd": 0, "ind": 1, "ty": 4, "nm": "heart",
            "sr": 1, "ks": {
                "o": {"a": 0, "k": 100},
                "r": {"a": 0, "k": 0},
                "p": {"a": 0, "k": [150, 150, 0]},
                "a": {"a": 0, "k": [0, 0, 0]},
                "s": {
                    "a": 1,
                    "k": [
                        {"t": 0, "s": [100, 100, 100]},
                        {"t": 30, "s": [115, 115, 100]},
                        {"t": 60, "s": [100, 100, 100]},
                        {"t": 90, "s": [115, 115, 100]}
                    ]
                }
            },
            "shapes": [
                {
                    "ty": "gr", "nm": "heart shape",
                    "it": [
                        {"ty": "fl", "c": {"a": 0, "k": [0.93, 0.18, 0.51, 1]}, "o": {"a": 0, "k": 100}},
                        {"ty": "tr", "p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}},
                        {
                            "ty": "sh", "ks": {
                                "a": 0,
                                "k": {
                                    "i": [[0, 0],[0, -55.5],[-55.5, 0],[0, 0],[0, -55.5],[-55.5, 0],[0,0]],
                                    "o": [[-55.5, 0],[0, 55.5],[0, 0],[-55.5, 0],[0, 55.5],[0,0],[0,0]],
                                    "v": [[0, -40],[ -40, -80],[ -80, -40],[ -80, 10],[ -40, 50],[0, 90],[40, 50]],
                                    "c": True
                                }
                            }
                        }
                    ]
                }
            ],
            "ao": 0
        }
    ]
}

lottie_medical = (
    load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_tutvdkg0.json")
    or load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_9x7s1x3g.json")
    or load_lottie_file("assets/medical.json")
    or INLINE_FALLBACK
)

# Header
GradientHeader(
    title="🩺 HealthScope",
    subtitle="Healthcare dashboards for exploring medical datasets",
    gradient=GRADIENT,
    height="320px"
)

col1, col2 = st.columns([1.2, 0.8], gap="large")

with col1:
    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <h3 style="color:{TEXT}; margin-top:0.5rem;">A healthcare dashboard for visualizing medical datasets</h3>
        <p style="font-size:1.05rem; color:#555;">
        Explore interactive dashboards for <b>PCOS</b>, <b>Diabetes</b>, and <b>Heart Disease</b>. 
        Visualize patterns and uncover insights — all in one place.
        </p>
        """,
        unsafe_allow_html=True
    )

with col2:
    st_lottie(lottie_medical, height=260, key="med_lottie")

# Dashboard Stats (kept as-is)
st.markdown("<hr style='margin-top:1.25rem; margin-bottom:0.75rem;'>", unsafe_allow_html=True)

@st.cache_data
def load_dataset(path):
    try:
        df = pd.read_csv(path)
    except Exception:
        df = pd.DataFrame()
    return df

@st.cache_data
def compute_stats(df: pd.DataFrame):
    if df.empty:
        return {"Rows": "0", "Columns": "0", "Missing": "0", "Numeric": "0", "Categorical": "0"}
    rows = df.shape[0]
    cols = df.shape[1]
    missing = int(df.isna().sum().sum())
    numeric_cols = df.select_dtypes(include=[np.number]).shape[1]
    categorical_cols = cols - numeric_cols
    return {
        "Rows": f"{rows:,}",
        "Columns": f"{cols}",
        "Missing": f"{missing}",
        "Numeric": f"{numeric_cols}",
        "Categorical": f"{categorical_cols}",
    }

heart_df = load_dataset("data/heart_disease.csv")
diabetes_df = load_dataset("data/diabetes.csv")
pcos_df = load_dataset("data/pcos_data.csv")

heart_stats = compute_stats(heart_df)
diabetes_stats = compute_stats(diabetes_df)
pcos_stats = compute_stats(pcos_df)

st.markdown(f"<h2 style='color:{TEXT}; text-align:center;'>Dashboard Statistics</h2>", unsafe_allow_html=True)

def stat_card(title, data, border_color):
    st.markdown(
        f"""
        <div style="
            background:rgba(255,255,255,0.88);
            padding:2rem;
            border-radius:20px;
            box-shadow:0 6px 18px rgba(0,0,0,0.06);
            border:3px solid {border_color};
        ">
            <div style="font-size:1.3rem; font-weight:700; color:{border_color}; margin-bottom:0.8rem;">{title} Dataset</div>
            <div style="font-size:1.05rem; color:#444;">Total Rows: <b>{data['Rows']}</b></div>
            <div style="font-size:1.05rem; color:#444;">Total Columns: <b>{data['Columns']}</b></div>
            <div style="font-size:1.05rem; color:#444;">Missing Values: <b>{data['Missing']}</b></div>
            <div style="font-size:1.05rem; color:#444;">Numerical Columns: <b>{data['Numeric']}</b></div>
            <div style="font-size:1.05rem; color:#444;">Categorical Columns: <b>{data['Categorical']}</b></div>
        </div>
        """,
        unsafe_allow_html=True
    )

c1, c2, c3 = st.columns(3)
with c1: stat_card("Heart Disease", heart_stats, "#D7263D")
with c2: stat_card("Diabetes", diabetes_stats, "#3B82F6")
with c3: stat_card("PCOS", pcos_stats, "#EC4899")

st.markdown("<hr style='margin-top:1.75rem; margin-bottom:1rem;'>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="text-align:center; font-size:0.95rem; color:#888; padding:1rem 2rem;">
    <i>This dashboard is intended for educational and exploratory purposes only. It does not provide medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional for medical concerns.</i>
    </div>
    """,
    unsafe_allow_html=True
)
