# Diabetes Dashboard (visualization-only)
import streamlit as st
import pandas as pd

from utils.layout import apply_custom_css, GradientHeader, Card, ResultCard, KPIBlock
from utils.themes import HealthScopeTheme as Theme
from utils.charts import (
    create_pie_chart,
    create_histogram,
    create_boxplot,
    create_correlation_heatmap,
)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Diabetes Dashboard",
    page_icon="💉",
    layout="wide"
)
apply_custom_css()

PRIMARY = Theme.DIABETES["primary"]
TEXT = Theme.DIABETES["text"]
LIGHT = Theme.DIABETES["light"]
GRADIENT = Theme.DIABETES["gradient"]
BG = "#FAFAFF"

ACCENT = "#8C7BFF"

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("data/diabetes.csv")

df = load_data()

# --------------------------------------------------
# HEADER
# --------------------------------------------------
GradientHeader(
    title="💉 Diabetes Dashboard",
    subtitle="Type 2 Diabetes data visualization and exploratory dashboard",
    gradient=GRADIENT,
    height="280px"
)

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

# --------------------------------------------------
# TABS — only Data Exploration now
# --------------------------------------------------
tab1 = st.container()

st.markdown(f"<h2 style='color:{TEXT}; margin-bottom:1rem;'>Dataset Overview</h2>", unsafe_allow_html=True)

left_col, right_col = st.columns([1, 1], gap="large")

with left_col:
    rows = df.shape[0]
    cols = df.shape[1]
    missing = int(df.isna().sum().sum())
    missing_pct = round((missing / max(1, rows * cols)) * 100, 2)
    avg_age = round(df["Age"].mean(), 1) if "Age" in df.columns else None
    avg_bmi = round(df["BMI"].mean(), 1) if "BMI" in df.columns else None
    diabetic_pct = round((df["Outcome"].sum() / rows) * 100, 1) if "Outcome" in df.columns else None

    def stat_block(label, value):
        st.markdown(
            f"""
            <div style="min-width:140px; margin-bottom:12px;">
                <div style="font-size:0.85rem; color:#6B7280; text-transform:uppercase;">{label}</div>
                <div style="font-size:1.5rem; font-weight:800; color:{PRIMARY};">{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    c1, c2, c3 = st.columns(3)
    with c1:
        stat_block("Rows", f"{rows:,}")
        stat_block("Missing", f"{missing} ({missing_pct}%)")

    with c2:
        stat_block("Columns", cols)
        stat_block("Average Age", avg_age or "N/A")

    with c3:
        stat_block("Avg BMI", avg_bmi or "N/A")
        stat_block("Diabetes %", f"{diabetic_pct}%" if diabetic_pct is not None else "N/A")

    st.markdown("### Quick Preview of the Dataset (first 5 rows)")
    st.dataframe(df.head(), use_container_width=True)

with right_col:
    st.markdown("### 📈 Interactive Graph Builder")

    all_cols = list(df.columns)
    x_axis = st.selectbox("X axis", all_cols, key="xaxis_diab")
    y_axis = st.selectbox("Y axis (optional)", ["None"] + all_cols, key="yaxis_diab")
    chart_type = st.selectbox("Chart type", ["Scatter", "Line", "Histogram", "Box", "Bar"], key="charttype_diab")

    if st.button("Generate Chart", use_container_width=True, key="gen_diab_chart"):
        try:
            import plotly.express as px

            if chart_type == "Scatter" and y_axis != "None":
                fig = px.scatter(df, x=x_axis, y=y_axis, color="Outcome" if "Outcome" in df.columns else None)
                st.plotly_chart(fig, use_container_width=True)

            elif chart_type == "Line" and y_axis != "None":
                fig = px.line(df, x=x_axis, y=y_axis)
                st.plotly_chart(fig, use_container_width=True)

            elif chart_type == "Histogram":
                fig = px.histogram(df, x=x_axis, nbins=30,
                                   color_discrete_sequence=[PRIMARY])
                st.plotly_chart(fig, use_container_width=True)

            elif chart_type == "Box" and y_axis != "None":
                fig = px.box(df, x=x_axis, y=y_axis)
                st.plotly_chart(fig, use_container_width=True)

            elif chart_type == "Bar":
                if y_axis != "None":
                    fig = px.bar(df, x=x_axis, y=y_axis)
                else:
                    agg = df[x_axis].value_counts().reset_index()
                    agg.columns = [x_axis, "count"]
                    fig = px.bar(agg, x=x_axis, y="count")
                st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Plot failed: {e}")

# --------------------------------------------------
# MINI VISUALIZATIONS BELOW
# --------------------------------------------------
st.markdown("---")
st.markdown(f"<h3 style='color:{TEXT};'>Quick Insights</h3>", unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    if "Outcome" in df.columns:
        outcome_counts = df["Outcome"].value_counts()
        pie = create_pie_chart(outcome_counts.values,
                               ["Non-Diabetic", "Diabetic"],
                               "Diabetes Distribution",
                               theme="diabetes")
        st.plotly_chart(pie, use_container_width=True)

    if "Glucose" in df.columns:
        hist_glucose = create_histogram(df, "Glucose",
                                        "Glucose Distribution",
                                        theme="diabetes")
        st.plotly_chart(hist_glucose, use_container_width=True)

with c2:
    if "BMI" in df.columns:
        box_bmi = create_boxplot(df, "BMI",
                                 "BMI Spread",
                                 theme="diabetes")
        st.plotly_chart(box_bmi, use_container_width=True)

    if "Insulin" in df.columns:
        insulin_nonzero = df[df["Insulin"] > 0]
        hist_insulin = create_histogram(insulin_nonzero,
                                        "Insulin",
                                        "Insulin Distribution",
                                        theme="diabetes")
        st.plotly_chart(hist_insulin, use_container_width=True)

st.markdown("---")
st.markdown(f"<h3 style='color:{TEXT};'>Additional Visualizations</h3>", unsafe_allow_html=True)

g1, g2 = st.columns(2)
with g1:
    if "Glucose" in df.columns:
        import plotly.express as px
        fig_glu = px.histogram(df, x="Glucose", nbins=30,
                               marginal="rug",
                               color_discrete_sequence=[PRIMARY])
        st.plotly_chart(fig_glu, use_container_width=True)

with g2:
    if "Outcome" in df.columns:
        counts = df["Outcome"].value_counts().reset_index()
        counts.columns = ["Outcome", "Count"]
        fig_cnt = px.bar(counts, x="Outcome", y="Count")
        st.plotly_chart(fig_cnt, use_container_width=True)

g3, g4 = st.columns(2)
with g3:
    if set(["BMI", "Glucose"]).issubset(df.columns):
        fig_sc = px.scatter(df, x="BMI", y="Glucose",
                            color="Outcome" if "Outcome" in df.columns else None)
        st.plotly_chart(fig_sc, use_container_width=True)

with g4:
    if set(["Outcome", "Age"]).issubset(df.columns):
        fig_bx = px.box(df, x="Outcome", y="Age",
                        color="Outcome" if "Outcome" in df.columns else None)
        st.plotly_chart(fig_bx, use_container_width=True)

st.markdown("---")
st.markdown(f"<h3 style='color:{TEXT};'>Correlation Heatmap</h3>", unsafe_allow_html=True)
corr_fig = create_correlation_heatmap(df,
                                      "Diabetes Feature Correlations",
                                      theme="diabetes")
st.plotly_chart(corr_fig, use_container_width=True)
