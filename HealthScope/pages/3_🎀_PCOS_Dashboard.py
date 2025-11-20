# PCOS Dashboard (visualization-only, fully optimized)
import streamlit as st
import pandas as pd
import plotly.express as px

from utils.layout import apply_custom_css, GradientHeader
from utils.themes import HealthScopeTheme as Theme
from utils.charts import (
    create_pie_chart,
    create_histogram,
    create_bar_chart
)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="PCOS Dashboard",
    page_icon="🎀",
    layout="wide"
)

apply_custom_css()

# THEME COLORS
PRIMARY = "#FF2E82"
SECONDARY = "#FF78B6"
ACCENT = "#FFD1E6"
TEXT = Theme.PCOS["text"]
GRADIENT = Theme.PCOS["gradient"]

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("data/pcos_data.csv")

df = load_data()

# --------------------------------------------------
# HEADER
# --------------------------------------------------
GradientHeader(
    title="🎀 PCOS Dashboard",
    subtitle="PCOS data visualization and exploratory dashboard",
    gradient=GRADIENT,
    height="330px"
)

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

# --------------------------------------------------
# DATA OVERVIEW
# --------------------------------------------------
st.markdown(f"<h2 style='color:{TEXT}; margin-bottom:1rem;'>Dataset Overview</h2>", unsafe_allow_html=True)

left_col, right_col = st.columns([1, 1], gap="large")

with left_col:
    rows = df.shape[0]
    cols = df.shape[1]
    missing = df.isna().sum().sum()
    avg_age = round(df["Age"].mean(), 1) if "Age" in df.columns else "N/A"
    avg_lifestyle = round(df["Lifestyle Score"].mean(), 1) if "Lifestyle Score" in df.columns else "N/A"
    risk_pct = (
        round((df["Risk"].value_counts().get("Yes", 0) / rows) * 100, 1)
        if "Risk" in df.columns else "N/A"
    )

    def stat(label, value):
        st.markdown(
            f"""
            <div style="margin-bottom:12px;">
                <div style="font-size:0.85rem; color:#6B7280;">{label}</div>
                <div style="font-size:1.6rem; font-weight:800; color:{PRIMARY};">{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    c1, c2, c3 = st.columns(3)
    with c1:
        stat("Rows", f"{rows:,}")
        stat("Missing", missing)
    with c2:
        stat("Columns", cols)
        stat("Avg Age", avg_age)
    with c3:
        stat("Avg Lifestyle", avg_lifestyle)
        stat("Risk %", f"{risk_pct}%" if risk_pct != "N/A" else "N/A")

    st.markdown("### Quick Preview")
    st.dataframe(df.head(), use_container_width=True)

# --------------------------------------------------
# GRAPH BUILDER
# --------------------------------------------------
with right_col:
    st.markdown("### 📈 Interactive Graph Builder")

    all_cols = list(df.columns)
    x_axis = st.selectbox("X axis", all_cols)
    y_axis = st.selectbox("Y axis (optional)", ["None"] + all_cols)
    chart_type = st.selectbox("Chart Type", ["Scatter", "Bar", "Histogram", "Box"])

    if st.button("Generate Chart", use_container_width=True):
        try:
            if chart_type == "Scatter" and y_axis != "None":
                fig = px.scatter(
                    df, x=x_axis, y=y_axis,
                    color="Risk" if "Risk" in df.columns else None,
                    color_discrete_map={"Yes": PRIMARY, "No": SECONDARY}
                )

            elif chart_type == "Bar":
                if y_axis != "None":
                    fig = px.bar(df, x=x_axis, y=y_axis, color_discrete_sequence=[PRIMARY])
                else:
                    vc = df[x_axis].value_counts().reset_index()
                    vc.columns = [x_axis, "count"]
                    fig = px.bar(vc, x=x_axis, y="count", color_discrete_sequence=[PRIMARY])

            elif chart_type == "Histogram":
                fig = px.histogram(df, x=x_axis, color_discrete_sequence=[PRIMARY])

            elif chart_type == "Box" and y_axis != "None":
                fig = px.box(df, x=x_axis, y=y_axis, color_discrete_sequence=[PRIMARY])

            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Error generating chart: {e}")

# --------------------------------------------------
# QUICK INSIGHTS
# --------------------------------------------------
st.markdown("---")
st.markdown(f"<h3 style='color:{TEXT};'>Quick Insights</h3>", unsafe_allow_html=True)

A, B = st.columns(2)

with A:
    if "Risk" in df.columns:
        rcounts = df["Risk"].value_counts()
        fig1 = create_pie_chart(
            rcounts.values,
            list(rcounts.index),
            "PCOS Risk Distribution",
            theme="pcos"
        )
        st.plotly_chart(fig1, use_container_width=True)

    if "Age" in df.columns:
        fig2 = create_histogram(df, "Age", "Age Distribution", theme="pcos")
        st.plotly_chart(fig2, use_container_width=True)

with B:
    if "Lifestyle Score" in df.columns:
        fig3 = create_histogram(df, "Lifestyle Score", "Lifestyle Score Distribution", theme="pcos")
        st.plotly_chart(fig3, use_container_width=True)

    # Find BMI column
    bmi_col = None
    for candidate in ["BMI", "BMI Category", "BMI Category "]:
        if candidate in df.columns:
            bmi_col = candidate
            break

    if bmi_col:
        bmi_counts = df[bmi_col].value_counts().head(5).reset_index()
        bmi_counts.columns = [bmi_col, "Count"]
        fig4 = create_bar_chart(
            data=bmi_counts,
            x_column=bmi_col,
            y_column="Count",
            title="BMI Category Distribution",
            theme="pcos"
        )
        st.plotly_chart(fig4, use_container_width=True)

# --------------------------------------------------
# ADDITIONAL VISUALIZATIONS (Optimized)
# --------------------------------------------------
st.markdown("---")
st.markdown(f"<h3 style='color:{TEXT};'>Additional Visualizations</h3>", unsafe_allow_html=True)

C, D = st.columns(2)

# --- FAST PLOTLY VERSION OF AGE VS UNDIAGNOSED ---
# --- FAST SEABORN-STYLE PLOTLY VERSION (IDENTICAL LOOK, INSTANT LOAD) ---
with C:
    if set(["Age", "Undiagnosed PCOS Likelihood"]).issubset(df.columns):
        import plotly.express as px
        import numpy as np

        # jitter to separate overlapping dots
        jitter_strength = 0.006
        y_vals = df["Undiagnosed PCOS Likelihood"].astype(float).values
        y_jittered = y_vals + np.random.normal(0, jitter_strength, len(y_vals))

        color_col = "Menstrual Regularity" if "Menstrual Regularity" in df.columns else None

        # Build figure with Seaborn-like style
        fig = px.scatter(
            df,
            x="Age",
            y=y_jittered,
            color=color_col,
            opacity=0.85,
            color_discrete_map={
                "Regular": PRIMARY,
                "Irregular": SECONDARY
            },
            labels={
                "Age": "Age",
                "y": "Undiagnosed PCOS Likelihood"
            },
            title="Age vs Undiagnosed PCOS Likelihood"
        )

        # Adjust marker size + borders to mimic seaborn
        fig.update_traces(marker=dict(size=8, line=dict(width=0.3, color="white")))

        # Clean, Seaborn-like layout
        fig.update_layout(
            height=500,
            xaxis_title="Age",
            yaxis_title="Undiagnosed PCOS Likelihood",
            plot_bgcolor="white",
            paper_bgcolor="rgba(0,0,0,0)",
            legend_title="Menstrual Regularity",
            margin=dict(l=20, r=20, t=60, b=40)
        )

        st.plotly_chart(fig, use_container_width=True)


# --- MENSTRUAL REGULARITY COUNT ---
with D:
    if "Menstrual Regularity" in df.columns:
        reg_counts = df["Menstrual Regularity"].value_counts().reset_index()
        reg_counts.columns = ["Menstrual Regularity", "Count"]

        fig_cnt = px.bar(
            reg_counts,
            x="Menstrual Regularity",
            y="Count",
            color="Menstrual Regularity",
            color_discrete_map={"Regular": PRIMARY, "Irregular": SECONDARY},
            title="Distribution of Menstrual Regularity"
        )

        st.plotly_chart(fig_cnt, use_container_width=True)

# --------------------------------------------------
# LIFESTYLE SCORE BY FAMILY HISTORY
# --------------------------------------------------
if set(["Family History of PCOS", "Lifestyle Score"]).issubset(df.columns):
    fig_box = px.box(
        df,
        x="Family History of PCOS",
        y="Lifestyle Score",
        color="Family History of PCOS",
        color_discrete_map={"Yes": PRIMARY, "No": SECONDARY},
        title="Lifestyle Score by Family History of PCOS"
    )
    st.plotly_chart(fig_box, use_container_width=True)
