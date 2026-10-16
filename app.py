"""
Cricbuzz LiveStats - Modern Sports Broadcast Analytics Portal
"""

import os
import sys
import streamlit as st

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.db_connection import execute_query, initialize_database
from utils.ui_theme import apply_theme, render_hero, render_kpi
from services.api_client import CricbuzzApiClient

# Page configuration
st.set_page_config(
    page_title="Cricbuzz LiveStats | Broadcast Analytics",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply global dark sports broadcast theme
apply_theme()


def main():
    # Hero Banner
    render_hero(
        title="🏏 Cricbuzz LiveStats",
        subtitle="Enterprise Real-Time Cricket Telemetry, REST Ingestion & 3NF SQL Analytics",
        badge_text="BROADCAST PRO"
    )

    # Sidebar System Health & Controls
    st.sidebar.markdown("### 📡 System Diagnostics")
    
    api_client = CricbuzzApiClient()
    if api_client.is_configured():
        st.sidebar.success("🟢 **Live Cricbuzz API:** Connected")
    else:
        st.sidebar.info("🟡 **Live Feed:** Realistic Simulator Mode")

    try:
        players_count = int(execute_query("SELECT COUNT(*) AS c FROM players;").iloc[0]['c'])
        matches_count = int(execute_query("SELECT COUNT(*) AS c FROM matches;").iloc[0]['c'])
        venues_count = int(execute_query("SELECT COUNT(*) AS c FROM venues;").iloc[0]['c'])
        teams_count = int(execute_query("SELECT COUNT(*) AS c FROM teams;").iloc[0]['c'])
        db_healthy = True
    except Exception as e:
        players_count = matches_count = venues_count = teams_count = 0
        db_healthy = False
        st.sidebar.error(f"Database error: {e}")

    if db_healthy:
        st.sidebar.success("🟢 **SQL Database:** Online (SQLite 3NF)")
    else:
        st.sidebar.error("🔴 **SQL Database:** Offline")
        if st.sidebar.button("Initialize / Repair Database"):
            initialize_database()
            st.rerun()

    # Re-seed option for learners
    with st.sidebar.expander("🛠️ Database Maintenance"):
        st.caption("Reset your database to the default seed data anytime.")
        if st.button("Reload Default Seed Data"):
            base_dir = os.path.dirname(os.path.abspath(__file__))
            seed_path = os.path.join(base_dir, "database", "seed_data.sql")
            initialize_database()
            with open(seed_path, "r", encoding="utf-8") as f:
                seed_sql = f.read()
            from utils.db_connection import get_db_connection
            with get_db_connection() as conn:
                conn.executescript(seed_sql)
            st.success("Database re-seeded successfully!")
            st.rerun()

    # Modern KPI Grid
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi("Registered Players", str(players_count), "🧢", "Active in Roster")
    with col2:
        render_kpi("Matches Tracked", str(matches_count), "🏟️", "Across 3 Formats")
    with col3:
        render_kpi("International Teams", str(teams_count), "🌍", "ICC Full Members")
    with col4:
        render_kpi("Global Venues", str(venues_count), "📍", "Capacity up to 132K")

    st.write("")
    st.write("")

    # Feature Modules Grid
    st.markdown("### ⚡ Telemetry & Analytical Modules")
    mcol1, mcol2 = st.columns(2)

    with mcol1:
        st.markdown("""
        <div class="module-card">
            <span class="module-icon">⚡</span>
            <div class="module-title">1. Live Matches & Real-Time Telemetry</div>
            <div class="module-desc">
                High-frequency live scorecards directly from the Cricbuzz REST feed. View run rates, active batsmen wagon metrics, current bowler economy, and sync live fixtures directly into your relational database.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        st.markdown("""
        <div class="module-card">
            <span class="module-icon">🔬</span>
            <div class="module-title">3. 25 Enterprise SQL Analytics Case Studies</div>
            <div class="module-desc">
                High-level query engine tackling 25 enterprise sports analytics problems. Features CTEs, Window Functions (<code>ROW_NUMBER</code>, <code>LAG</code>), Standard Deviation consistency metrics, and custom SQL sandbox.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with mcol2:
        st.markdown("""
        <div class="module-card">
            <span class="module-icon">📊</span>
            <div class="module-title">2. Top Player Stats & Leaderboards</div>
            <div class="module-desc">
                Comprehensive leaderboard hub comparing performers across Test, ODI, and T20I formats. Explore most runs, bowling averages, boundary conversion, and batting partnership standouts with Plotly visualizations.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        st.markdown("""
        <div class="module-card">
            <span class="module-icon">🛠️</span>
            <div class="module-title">4. Administrative Data Governance (CRUD)</div>
            <div class="module-desc">
                Interactive control panel for registering new cricket talent, managing player profiles, tracking retirements, and performing transactional soft deletes to guarantee relational integrity.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    # Recent Matches Highlights Strip
    st.markdown("### 🏆 Recent Match Highlights")
    recent_matches = execute_query("""
        SELECT 
            m.match_description,
            m.match_format,
            m.match_date,
            t1.team_short_name AS t1_code,
            t2.team_short_name AS t2_code,
            COALESCE(tw.team_name, 'No Result') AS winner,
            m.victory_margin,
            m.victory_type,
            v.venue_name,
            v.city
        FROM matches m
        JOIN teams t1 ON m.team1_id = t1.team_id
        JOIN teams t2 ON m.team2_id = t2.team_id
        LEFT JOIN teams tw ON m.winner_team_id = tw.team_id
        JOIN venues v ON m.venue_id = v.venue_id
        WHERE m.match_status = 'Completed'
        ORDER BY m.match_date DESC
        LIMIT 3;
    """)

    if not recent_matches.empty:
        rcols = st.columns(len(recent_matches))
        for idx, row in recent_matches.iterrows():
            with rcols[idx]:
                st.markdown(f"""
                <div class="match-card">
                    <div class="match-header">
                        <span class="series-title">{row['t1_code']} vs {row['t2_code']}</span>
                        <span class="format-pill {row['match_format'].lower()}">{row['match_format']}</span>
                    </div>
                    <div style="font-size: 0.95rem; font-weight: 700; color: #F8FAFC; margin-bottom: 6px;">
                        {row['match_description']}
                    </div>
                    <div style="font-size: 0.82rem; color: #94A3B8; margin-bottom: 12px;">
                        📍 {row['venue_name']}, {row['city']}
                    </div>
                    <div class="status-banner">
                        <span>🏆 Winner: <b>{row['winner']}</b></span>
                        <span style="color: #10B981;">by {row['victory_margin']} {row['victory_type']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
