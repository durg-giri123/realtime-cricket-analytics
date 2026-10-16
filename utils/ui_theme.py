"""
UI Design System & Styling Engine for Cricbuzz LiveStats.
Provides broadcast-grade dark sports styling, glassmorphic cards,
pulsing live badges, typography, and unified Plotly chart themes.
"""

import streamlit as st

# Custom Dark Sports Broadcast CSS
GLOBAL_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap');

    /* Global Typography & Root Settings */
    html, body, [class*="css"] {
        font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at 15% 15%, #111A2E 0%, #080D1A 60%, #050811 100%);
        color: #E2E8F0;
    }

    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em !important;
    }

    /* Hero / Title Bar */
    .hero-container {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 24px 28px;
        margin-bottom: 24px;
        backdrop-filter: blur(16px);
        box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }

    .hero-container::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 3px;
        background: linear-gradient(90deg, #10B981, #06B6D4, #F59E0B, #EC4899);
    }

    .hero-title {
        font-size: 2.2rem;
        font-weight: 900;
        margin: 0;
        background: linear-gradient(135deg, #FFFFFF 30%, #94A3B8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .hero-subtitle {
        color: #94A3B8;
        font-size: 1.05rem;
        margin-top: 6px;
        font-weight: 500;
    }

    /* Live Pulsing Badge */
    .live-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(239, 68, 68, 0.15);
        color: #F87171;
        border: 1px solid rgba(239, 68, 68, 0.35);
        border-radius: 999px;
        padding: 4px 12px;
        font-size: 0.75rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .live-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #EF4444;
        box-shadow: 0 0 10px #EF4444;
        animation: pulseDot 1.5s infinite;
    }

    @keyframes pulseDot {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.4; transform: scale(0.85); }
    }

    /* Modern KPI Cards */
    .kpi-card {
        background: linear-gradient(145deg, #131D31 0%, #0D1525 100%);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 16px;
        padding: 20px;
        position: relative;
        overflow: hidden;
        transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }

    .kpi-card:hover {
        transform: translateY(-3px);
        border-color: rgba(16, 185, 129, 0.4);
        box-shadow: 0 12px 28px rgba(0, 0, 0, 0.45);
    }

    .kpi-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }

    .kpi-label {
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #94A3B8;
    }

    .kpi-icon {
        font-size: 1.4rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        width: 38px;
        height: 38px;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }

    .kpi-value {
        font-size: 2.3rem;
        font-weight: 900;
        color: #F8FAFC;
        line-height: 1;
        font-variant-numeric: tabular-nums;
    }

    .kpi-delta {
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 8px;
        color: #10B981;
    }

    /* Broadcast Match Scorecard Card */
    .match-card {
        background: linear-gradient(145deg, #141E34 0%, #0F172A 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 22px;
        margin-bottom: 20px;
        position: relative;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    .match-card:hover {
        border-color: rgba(6, 182, 212, 0.4);
        transform: translateY(-2px);
    }

    .match-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        padding-bottom: 12px;
        margin-bottom: 16px;
    }

    .series-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #94A3B8;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .format-pill {
        display: inline-block;
        padding: 3px 9px;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        background: rgba(99, 102, 241, 0.15);
        color: #818CF8;
        border: 1px solid rgba(99, 102, 241, 0.3);
    }

    .format-pill.test { background: rgba(245, 158, 11, 0.15); color: #FBBF24; border-color: rgba(245, 158, 11, 0.3); }
    .format-pill.odi { background: rgba(16, 185, 129, 0.15); color: #34D399; border-color: rgba(16, 185, 129, 0.3); }
    .format-pill.t20 { background: rgba(236, 72, 153, 0.15); color: #F472B6; border-color: rgba(236, 72, 153, 0.3); }

    .team-score-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 0;
    }

    .team-badge {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .team-monogram {
        width: 36px;
        height: 36px;
        border-radius: 8px;
        background: linear-gradient(135deg, #1E293B, #334155);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 900;
        font-size: 0.9rem;
        color: #F8FAFC;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .team-name {
        font-size: 1.15rem;
        font-weight: 700;
        color: #F1F5F9;
    }

    .score-box {
        text-align: right;
    }

    .score-runs {
        font-size: 1.5rem;
        font-weight: 900;
        color: #FFFFFF;
        font-family: 'JetBrains Mono', monospace;
    }

    .score-overs {
        font-size: 0.8rem;
        font-weight: 600;
        color: #64748B;
        font-family: 'JetBrains Mono', monospace;
    }

    .status-banner {
        margin-top: 14px;
        padding: 10px 14px;
        border-radius: 10px;
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.05);
        font-size: 0.88rem;
        font-weight: 600;
        color: #38BDF8;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    /* Feature Grid Boxes */
    .module-card {
        background: linear-gradient(145deg, #131E33 0%, #0E1626 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 24px;
        height: 100%;
        position: relative;
        overflow: hidden;
        transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }

    .module-card:hover {
        transform: translateY(-4px);
        border-color: rgba(16, 185, 129, 0.5);
        box-shadow: 0 16px 32px rgba(0, 0, 0, 0.5);
    }

    .module-card::after {
        content: '';
        position: absolute;
        bottom: 0; left: 0; right: 0; height: 2px;
        background: linear-gradient(90deg, transparent, rgba(16, 185, 129, 0.4), transparent);
    }

    .module-icon {
        font-size: 2rem;
        margin-bottom: 12px;
        display: inline-block;
    }

    .module-title {
        font-size: 1.25rem;
        font-weight: 800;
        color: #F8FAFC;
        margin-bottom: 8px;
    }

    .module-desc {
        font-size: 0.9rem;
        color: #94A3B8;
        line-height: 1.6;
    }

    /* Streamlit Tabs Customization */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(15, 23, 42, 0.6);
        padding: 6px;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.06);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 8px 16px;
        color: #94A3B8 !important;
        font-weight: 700 !important;
        font-size: 0.88rem !important;
        border: none !important;
        background-color: transparent !important;
        transition: all 0.2s ease;
    }

    .stTabs [aria-selected="true"] {
        background-color: #1E293B !important;
        color: #F8FAFC !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 0.88rem !important;
        transition: all 0.2s ease !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25) !important;
    }

    /* Streamlit Dataframes */
    [data-testid="stDataFrame"] {
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 14px !important;
        overflow: hidden !important;
    }
</style>
"""


def apply_theme():
    """Injects the global sports broadcast CSS theme into the current page."""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def get_plotly_layout() -> dict:
    """Returns a unified, modern dark sports layout dictionary for Plotly charts."""
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(19, 29, 49, 0.4)",
        font=dict(family="Outfit, sans-serif", color="#CBD5E1", size=12),
        margin=dict(l=40, r=40, t=50, b=40),
        xaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.06)",
            linecolor="rgba(255, 255, 255, 0.1)",
            zerolinecolor="rgba(255, 255, 255, 0.1)",
            tickfont=dict(color="#94A3B8")
        ),
        yaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.06)",
            linecolor="rgba(255, 255, 255, 0.1)",
            zerolinecolor="rgba(255, 255, 255, 0.1)",
            tickfont=dict(color="#94A3B8")
        ),
        colorway=["#10B981", "#06B6D4", "#F59E0B", "#EC4899", "#8B5CF6", "#3B82F6"]
    )


def render_hero(title: str, subtitle: str, badge_text: str = None, is_live: bool = False):
    """Renders a stadium-style hero banner."""
    badge_html = ""
    if badge_text:
        if is_live:
            badge_html = f'<div class="live-badge"><div class="live-dot"></div>{badge_text}</div>'
        else:
            badge_html = f'<div class="format-pill odi">{badge_text}</div>'

    html = f"""
    <div class="hero-container">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px;">
            <div>
                <div class="hero-title">{title}</div>
                <div class="hero-subtitle">{subtitle}</div>
            </div>
            {badge_html}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_kpi(label: str, value: str, icon: str, delta: str = None):
    """Renders a sleek sports KPI card."""
    delta_html = f'<div class="kpi-delta">{delta}</div>' if delta else ""
    html = f"""
    <div class="kpi-card">
        <div class="kpi-header">
            <span class="kpi-label">{label}</span>
            <span class="kpi-icon">{icon}</span>
        </div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
