import streamlit as st
from utils.themes import HealthScopeTheme as Theme

# -------------------------------------------------------
# GLOBAL CSS
# -------------------------------------------------------
def apply_custom_css():
    st.markdown(f"""
    <style>
    .gradient-header, .gradient-header * {{
        cursor: default !important;
    }}
    html, body, .block-container, [data-testid="stAppViewContainer"] {{
        overflow-x: hidden !important;
        max-width: 100% !important;
    }}
    div {{
        box-sizing: border-box !important;
    }}
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    * {{
        font-family: {Theme.FONT_FAMILY};
    }}
    .element-container {{
        animation: hs_fadeIn 0.45s ease-in-out;
    }}
    @keyframes hs_fadeIn {{
        from {{ opacity: 0; transform: translateY(8px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    ::-webkit-scrollbar-thumb {{
        background: {Theme.HOME['primary']};
        border-radius: 999px;
    }}
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    @media (max-width: 768px) {{
        .hs-hero-desc {{ 
            margin-left: 16px !important; 
            max-width: 90% !important; 
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

# -------------------------------------------------------
# GRADIENT HEADER
# -------------------------------------------------------
def GradientHeader(title, subtitle, gradient, height='280px'):
    st.markdown(
        f"""
        <div style="
            background: {gradient};
            border-radius: 24px;
            padding: 2rem 2.5rem;
            text-align: center;
            color: white;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
            min-height: {height};
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        ">
            <div style="font-size: 3rem; font-weight: 800; margin: 0;">{title}</div>
            <div style="font-size: 1.25rem; margin-top: 0.75rem; opacity: 0.9; font-weight: 400;">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True
    )



# -------------------------------------------------------
# GLASS CONTAINER (optional helper)
# -------------------------------------------------------
def glass_container_inner(content, bg='rgba(255,255,255,0.55)'):
    st.markdown(f"""
        <div style="
            background: {bg};
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            padding: {Theme.SPACING['lg']};
            border-radius: {Theme.RADIUS['xl']};
            box-shadow: {Theme.SHADOWS['md']};
        ">
            {content}
        </div>
    """, unsafe_allow_html=True)



# -------------------------------------------------------
# KPI BLOCK (pastel animated stats)
# -------------------------------------------------------
def KPIBlock(title, value, subtitle, icon, theme='home'):
    theme_colors = getattr(Theme, theme.upper(), Theme.HOME)

    st.markdown(f"""
        <style>
        @keyframes countUp {{
            0% {{ opacity: 0; transform: translateY(6px); }}
            100% {{ opacity: 1; transform: translateY(0); }}
        }}
        </style>

        <div style="
            background: linear-gradient(135deg, {theme_colors['primary']}18, #ffffffdd);
            backdrop-filter: blur(14px);
            padding: 1.7rem;
            border-radius: 22px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.08);
            border: 1px solid {theme_colors['primary']}35;
            transition: 0.25s ease;
        "
        onmouseover="this.style.transform='translateY(-6px) scale(1.02)'"
        onmouseout="this.style.transform='translateY(0) scale(1)'">

            <div style="font-size: 2.6rem; opacity:0.92; margin-bottom: 6px;">
                {icon}
            </div>

            <p style="
                margin: 0;
                font-size: 0.8rem;
                font-weight: 700;
                text-transform: uppercase;
                color: #6b7280;
                letter-spacing: 0.55px;
            ">{title}</p>

            <h2 style="
                margin-top: 4px;
                font-size: 2.5rem;
                font-weight: 800;
                color: {theme_colors['primary']};
                animation: countUp 0.6s ease-out;
            ">{value}</h2>

            <p style="
                margin-top: 6px;
                font-size: 0.85rem;
                color: #94A3B8;
                line-height: 1.35;
            ">{subtitle}</p>

        </div>
    """, unsafe_allow_html=True)



# -------------------------------------------------------
# RESTORED CARD COMPONENT  (needed for dashboards)
# -------------------------------------------------------
def Card(content, background='white', padding='1.3rem', border_radius='1rem', shadow='md', hover=True):
    """Lightweight reusable UI card"""
    hover_style = (
        "transform: translateY(-4px); box-shadow: 0 8px 22px rgba(0,0,0,0.08);"
        if hover else ""
    )

    st.markdown(f"""
        <div style="
            background: {background};
            padding: {padding};
            border-radius: {border_radius};
            box-shadow: 0 4px 12px rgba(0,0,0,0.06);
            transition: all 0.25s ease;
            margin-bottom: 1rem;
        "
        onmouseover="this.style.cssText += '{hover_style}'"
        onmouseout="this.style.cssText = this.style.cssText.replace('{hover_style}', '')">
            {content}
        </div>
    """, unsafe_allow_html=True)



# -------------------------------------------------------
# RESULT CARD (placeholder to avoid import errors)
# -------------------------------------------------------
def ResultCard(title="", value="", icon="", subtitle=""):
    st.markdown(f"""
        <div style="
            background:white;
            padding:1rem;
            border-radius:14px;
            box-shadow:0 4px 12px rgba(0,0,0,0.06);
            margin-bottom:1rem;
        ">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <p style="margin:0; font-size:0.8rem; color:#64748B;">{title}</p>
                    <h3 style="margin:4px 0 0 0;">{value}</h3>
                </div>
                <div style="font-size:1.8rem;">{icon}</div>
            </div>
            <p style="margin-top:6px; color:#94A3B8; font-size:0.85rem;">{subtitle}</p>
        </div>
    """, unsafe_allow_html=True)
