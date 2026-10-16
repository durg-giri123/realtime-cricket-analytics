"""
Cricbuzz LiveStats - Broadcast Live Match Scorecards & Telemetry Ingestion
"""

import os
import sys
import streamlit as st
import pandas as pd

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.api_client import CricbuzzApiClient
from utils.db_connection import execute_query, execute_dml
from utils.ui_theme import apply_theme, render_hero

st.set_page_config(page_title="Live Matches | Cricbuzz LiveStats", page_icon="⚡", layout="wide")
apply_theme()

# Broadcast Hero Banner with Pulsing Live Badge
render_hero(
    title="⚡ Live Matches & Real-Time Telemetry",
    subtitle="Continuous REST stream ingestion with ball-by-ball scorecards and active pitch metrics",
    badge_text="LIVE ON AIR",
    is_live=True
)

# Sidebar Controls
st.sidebar.markdown("### 🎛️ Feed & Ingestion Controls")
api_client = CricbuzzApiClient()

user_key = st.sidebar.text_input("Custom RapidAPI Key", type="password", help="Overrides .env RAPIDAPI_KEY for this session")
if user_key:
    api_client.api_key = user_key

col_act1, col_act2 = st.columns([2, 10])
with col_act1:
    if st.button("🔄 Refresh Live Feed", type="primary"):
        st.cache_data.clear()
        st.rerun()

with st.spinner("Streaming real-time telemetry from Cricbuzz API..."):
    matches = api_client.get_live_matches()

if not matches:
    st.warning("No live matches currently streaming from the feed.")
else:
    st.caption(f"Broadcasting **{len(matches)}** active/recent match feeds • Engine: `{matches[0].get('source', 'Cricbuzz REST API')}`")

    for idx, match in enumerate(matches):
        fmt = match.get('format', 'T20').lower()
        fmt_class = "test" if "test" in fmt else "odi" if "odi" in fmt else "t20"

        # Broadcast Scorecard Container
        st.markdown(f"""
        <div class="match-card">
            <div class="match-header">
                <span class="series-title">
                    <span>🏆</span> {match.get('series_name')} • <b>{match.get('match_desc')}</b>
                </span>
                <span class="format-pill {fmt_class}">{match.get('format')}</span>
            </div>
            
            <div class="team-score-row">
                <div class="team-badge">
                    <div class="team-monogram">{match.get('team1_short', 'T1')[:3]}</div>
                    <span class="team-name">{match.get('team1')}</span>
                </div>
                <div class="score-box">
                    <span class="score-runs">{match.get('team1_runs', 0)}/{match.get('team1_wickets', 0)}</span>
                    <span class="score-overs">({match.get('team1_overs', 0.0)} ov)</span>
                </div>
            </div>

            <div class="team-score-row" style="margin-top: 6px;">
                <div class="team-badge">
                    <div class="team-monogram">{match.get('team2_short', 'T2')[:3]}</div>
                    <span class="team-name">{match.get('team2')}</span>
                </div>
                <div class="score-box">
                    <span class="score-runs">{match.get('team2_runs', 0)}/{match.get('team2_wickets', 0)}</span>
                    <span class="score-overs">({match.get('team2_overs', 0.0)} ov)</span>
                </div>
            </div>

            <div class="status-banner">
                <span>📍 {match.get('venue')}, {match.get('city')}</span>
                <span style="color: #38BDF8; font-weight: 700;">📢 {match.get('status')}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Active Pitch Breakdown
        batters = match.get('current_batters', [])
        bowler = match.get('current_bowler', {})

        if batters or bowler:
            bcol1, bcol2 = st.columns([3, 2])
            with bcol1:
                if batters:
                    st.markdown("##### 🏏 Active Batters at the Crease")
                    b_df = pd.DataFrame(batters)
                    st.dataframe(b_df, hide_index=True, use_container_width=True)
            with bcol2:
                if bowler:
                    st.markdown("##### 🎯 Current Bowler Spell")
                    bw_df = pd.DataFrame([bowler])
                    st.dataframe(bw_df, hide_index=True, use_container_width=True)

        # Ingestion Action
        with st.expander("📥 Ingest Match Summary into 3NF Database"):
            st.caption("Sync this live encounter into your local relational SQL tables for permanent query analysis.")
            if st.button(f"Sync Match #{match.get('match_id')} to Database", key=f"ingest_{idx}"):
                try:
                    # Check venue
                    venue_df = execute_query("SELECT venue_id FROM venues WHERE venue_name LIKE ?", (f"%{match.get('venue')}%",))
                    if not venue_df.empty:
                        vid = int(venue_df.iloc[0]['venue_id'])
                    else:
                        vid = execute_dml(
                            "INSERT INTO venues (venue_name, city, country, capacity) VALUES (?, ?, ?, ?)",
                            (match.get('venue'), match.get('city'), "International", 35000)
                        )

                    # Check teams
                    t1_df = execute_query("SELECT team_id FROM teams WHERE team_name = ?", (match.get('team1'),))
                    t1_id = int(t1_df.iloc[0]['team_id']) if not t1_df.empty else execute_dml(
                        "INSERT INTO teams (team_name, team_short_name, country) VALUES (?, ?, ?)",
                        (match.get('team1'), match.get('team1_short'), match.get('team1'))
                    )

                    t2_df = execute_query("SELECT team_id FROM teams WHERE team_name = ?", (match.get('team2'),))
                    t2_id = int(t2_df.iloc[0]['team_id']) if not t2_df.empty else execute_dml(
                        "INSERT INTO teams (team_name, team_short_name, country) VALUES (?, ?, ?)",
                        (match.get('team2'), match.get('team2_short'), match.get('team2'))
                    )

                    # Insert match
                    execute_dml("""
                        INSERT INTO matches (
                            match_description, match_format, match_date,
                            venue_id, team1_id, team2_id, match_status
                        ) VALUES (?, ?, date('now'), ?, ?, ?, 'Live')
                    """, (
                        f"{match.get('series_name')} - {match.get('match_desc')}",
                        match.get('format', 'T20I'),
                        vid, t1_id, t2_id
                    ))
                    st.success(f"Match #{match.get('match_id')} synced into SQLite database successfully!")
                except Exception as e:
                    st.error(f"Ingestion error: {e}")

        st.write("")
