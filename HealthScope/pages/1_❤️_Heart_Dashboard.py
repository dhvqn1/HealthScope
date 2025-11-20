# Heart Disease Dashboard (visualization-only)
import streamlit as st
import pandas as pd
import numpy as np

# Prefer Plotly for interactivity
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except Exception:
    PLOTLY_AVAILABLE = False

# Local utils
from utils.layout import apply_custom_css, GradientHeader
from utils.themes import HealthScopeTheme as Theme

# -------------------------
# Page config + global style
# -------------------------
st.set_page_config(page_title="Heart Disease Dashboard", page_icon="❤️", layout="wide")
apply_custom_css()

# Theme colors (deep elegant red)
PRIMARY = "#D7263D"
ACCENT = "#FF9090"
DARK = "#7A0A0A"
BG = "#FBFBFB"

# -------------------------
# Data
# -------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/heart_disease.csv")
    df = df.copy()
    df.fillna(0, inplace=True)
    return df

df = load_data()

# -------------------------
# Header
# -------------------------
GradientHeader(
    title="❤️ Heart Disease Analysis",
    subtitle="Cardiovascular data visualization and exploratory dashboard",
    gradient=Theme.HEART["gradient"],
    height="300px"
)
st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

# -------------------------
# Single tab (visuals only)
# -------------------------
st.markdown("## 📊 Dashboard Overview")

left_col, right_col = st.columns([1, 1], gap="large")

with left_col:
    rows = df.shape[0]
    cols = df.shape[1]
    missing = int(df.isna().sum().sum())
    missing_pct = round((missing / max(1, rows * cols)) * 100, 2)
    numeric_cols = df.select_dtypes(include=np.number).shape[1]
    cat_cols = df.select_dtypes(exclude=np.number).shape[1]
    avg_age = round(df["age"].mean(), 1)
    target_counts = df["target"].value_counts()
    target_pct = round((target_counts.get(1, 0) / rows) * 100, 1)

    stat_color = PRIMARY

    def stat_block(label, value):
        st.markdown(
            f"""
            <div style="min-width:140px; margin-bottom:12px;">
                <div style="font-size:0.85rem; color:#6B7280; text-transform:uppercase;">{label}</div>
                <div style="font-size:1.5rem; font-weight:800; color:{stat_color};">{value}</div>
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
        stat_block("Average Age", avg_age)

    with c3:
        stat_block("Numeric / Categorical", f"{numeric_cols} / {cat_cols}")
        stat_block("Target % (Has Disease)", f"{target_pct}%")

    st.markdown("### Quick preview of the dataset")
    st.dataframe(df.head(), use_container_width=True)

with right_col:
    st.markdown("### 📈 Interactive Graph Builder")

    all_cols = list(df.columns)
    x_axis = st.selectbox("X axis", all_cols, key="x_axis")
    y_axis = st.selectbox("Y axis (optional)", ["None"] + all_cols, key="y_axis")
    chart_type = st.selectbox("Chart type", ["Scatter", "Line", "Histogram", "Box", "Bar"], key="chart_type")

    if st.button("Generate", use_container_width=True, key="generate_btn"):
        if not PLOTLY_AVAILABLE:
            st.warning("Plotly not installed.")
        else:
            try:
                if chart_type == "Scatter" and y_axis != "None":
                    fig = px.scatter(df, x=x_axis, y=y_axis,
                                     color="target",
                                     color_discrete_sequence=[PRIMARY, ACCENT])
                    st.plotly_chart(fig, use_container_width=True)

                elif chart_type == "Line" and y_axis != "None":
                    fig = px.line(df, x=x_axis, y=y_axis)
                    fig.update_traces(line_color=PRIMARY)
                    st.plotly_chart(fig, use_container_width=True)

                elif chart_type == "Histogram":
                    fig = px.histogram(df, x=x_axis, nbins=30,
                                       color_discrete_sequence=[PRIMARY])
                    st.plotly_chart(fig, use_container_width=True)

                elif chart_type == "Box" and y_axis != "None":
                    fig = px.box(df, x=x_axis, y=y_axis,
                                 color_discrete_sequence=[PRIMARY])
                    st.plotly_chart(fig, use_container_width=True)

                elif chart_type == "Bar":
                    if y_axis != "None":
                        fig = px.bar(df, x=x_axis, y=y_axis,
                                     color_discrete_sequence=[PRIMARY])
                    else:
                        agg = df[x_axis].value_counts().reset_index()
                        agg.columns = [x_axis, "count"]
                        fig = px.bar(agg, x=x_axis, y="count",
                                     color_discrete_sequence=[PRIMARY])
                    st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error(f"Plotting failed: {e}")

# Compact Visualizations
st.markdown("---")
st.markdown("### Compact Visualizations — Quick Insights")

# Row 1 – Donut charts
r1c1, r1c2 = st.columns(2)
with r1c1:
    st.markdown("#### Heart Disease Distribution")
    tgt = df["target"].value_counts()
    fig = go.Figure(data=[go.Pie(
        labels=["No Disease", "Has Disease"],
        values=[tgt.get(0, 0), tgt.get(1, 0)],
        hole=0.45,
        marker=dict(colors=[ACCENT, PRIMARY])
    )])
    st.plotly_chart(fig, use_container_width=True)

with r1c2:
    st.markdown("#### Chest Pain Type Distribution")
    cp_counts = df["cp"].value_counts().sort_index()
    fig = go.Figure(data=[go.Pie(
        labels=[f"Type {i}" for i in cp_counts.index],
        values=cp_counts.values,
        hole=0.45,
        marker=dict(colors=[ACCENT, PRIMARY, "#FF6B6B", "#FF4A4A"])
    )])
    st.plotly_chart(fig, use_container_width=True)

# Row 2 – Histograms
r2c1, r2c2 = st.columns(2)
with r2c1:
    st.markdown("#### Age Distribution")
    fig = px.histogram(df, x="age", nbins=30, color_discrete_sequence=[PRIMARY])
    st.plotly_chart(fig, use_container_width=True)

with r2c2:
    st.markdown("#### Cholesterol Distribution")
    fig = px.histogram(df, x="chol", nbins=30, color_discrete_sequence=[ACCENT])
    st.plotly_chart(fig, use_container_width=True)

# Row 3 – Boxplot + Count
r3c1, r3c2 = st.columns(2)
with r3c1:
    st.markdown("#### Resting BP by Target")
    fig = px.box(df, x="target", y="trestbps",
                 color="target",
                 color_discrete_map={0: ACCENT, 1: PRIMARY})
    st.plotly_chart(fig, use_container_width=True)

with r3c2:
    st.markdown("#### Target Counts")
    fig = px.histogram(df, x="target", nbins=2, color_discrete_sequence=[PRIMARY])
    st.plotly_chart(fig, use_container_width=True)

# Row 4 – Scatter + Age Histogram
r4c1, r4c2 = st.columns(2)
with r4c1:
    st.markdown("#### Cholesterol vs Max Heart Rate")
    fig = px.scatter(df, x="chol", y="thalach",
                     color="target",
                     color_discrete_sequence=[ACCENT, PRIMARY])
    st.plotly_chart(fig, use_container_width=True)

with r4c2:
    st.markdown("#### Age Histogram (Compact)")
    fig = px.histogram(df, x="age", nbins=25, color_discrete_sequence=[ACCENT])
    st.plotly_chart(fig, use_container_width=True)

# Full-width correlation heatmap
st.markdown("---")
st.markdown("### ❤️ Heart Disease Feature Correlations")

corr = df.corr(numeric_only=True)

if PLOTLY_AVAILABLE:
    fig = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale="Reds",
        aspect="auto",
    )

    fig.update_layout(
        height=900,
        width=None,
        margin=dict(l=0, r=0, t=40, b=40),
        coloraxis_colorbar=dict(
            thickness=18,
            outlinewidth=0,
            ticks="outside",
        )
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    import seaborn as sns
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(22, 14))
    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="Reds",
        linewidths=0.5,
        cbar_kws={"shrink": 0.6},
        ax=ax
    )
    st.pyplot(fig, use_container_width=True)
