"""
Cricbuzz LiveStats - Broadcast Player Leaderboards & Benchmark Records
"""

import os
import sys
import streamlit as st
import pandas as pd
import plotly.express as px

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db_connection import execute_query
from utils.ui_theme import apply_theme, render_hero, get_plotly_layout

st.set_page_config(page_title="Top Stats | Cricbuzz LiveStats", page_icon="📊", layout="wide")
apply_theme()

render_hero(
    title="📊 Top Player Stats & Benchmark Records",
    subtitle="Cross-format leaderboards, historical milestones, and player efficiency matrices",
    badge_text="LEADERBOARDS"
)

# Format Filter in Sidebar
st.sidebar.markdown("### 🎯 Format Filter")
format_filter = st.sidebar.selectbox("Select Cricket Format", ["All Formats", "Test", "ODI", "T20I"])

format_clause = ""
format_param = ()
if format_filter != "All Formats":
    format_clause = "WHERE m.match_format = ?"
    format_param = (format_filter,)

tab_runs, tab_wickets, tab_power, tab_high, tab_parts = st.tabs([
    "🏏 Top Run Scorers",
    "🎯 Top Wicket Takers",
    "💥 Power Hitters (Strike Rate)",
    "⭐ Highest Individual Innings",
    "🤝 Record Partnerships"
])

# 1. Top Run Scorers
with tab_runs:
    st.markdown(f"#### 🏏 Top Run Scorers • {format_filter}")
    sql_runs = f"""
        SELECT 
            p.full_name AS Player,
            t.team_short_name AS Team,
            SUM(b.runs_scored) AS Total_Runs,
            COUNT(b.performance_id) AS Innings,
            ROUND(CAST(SUM(b.runs_scored) AS REAL) / NULLIF(COUNT(CASE WHEN b.dismissal_status != 'not out' THEN 1 END), 0), 2) AS Batting_Avg,
            ROUND(AVG(b.strike_rate), 2) AS Strike_Rate,
            SUM(b.fours) AS Fours,
            SUM(b.sixes) AS Sixes,
            SUM(CASE WHEN b.runs_scored >= 100 THEN 1 ELSE 0 END) AS Centuries
        FROM batting_scorecards b
        JOIN players p ON b.player_id = p.player_id
        JOIN teams t ON p.team_id = t.team_id
        JOIN matches m ON b.match_id = m.match_id
        {format_clause}
        GROUP BY p.player_id, p.full_name, t.team_short_name
        ORDER BY Total_Runs DESC
        LIMIT 10;
    """
    df_runs = execute_query(sql_runs, format_param)
    if not df_runs.empty:
        col_tbl, col_chart = st.columns([6, 5])
        with col_tbl:
            st.dataframe(df_runs, hide_index=True, use_container_width=True)
        with col_chart:
            fig_runs = px.bar(
                df_runs,
                x="Total_Runs",
                y="Player",
                orientation="h",
                color="Total_Runs",
                color_continuous_scale="Teal",
                title="Runs Scored Leaderboard",
                labels={"Total_Runs": "Total Runs Scored"}
            )
            fig_runs.update_layout(**get_plotly_layout())
            fig_runs.update_layout(yaxis={'categoryorder': 'total ascending'}, height=380)
            st.plotly_chart(fig_runs, use_container_width=True)
    else:
        st.info("No records found for the selected filter.")

# 2. Top Wicket Takers
with tab_wickets:
    st.markdown(f"#### 🎯 Top Wicket Takers • {format_filter}")
    sql_wickets = f"""
        SELECT 
            p.full_name AS Bowler,
            t.team_short_name AS Team,
            SUM(bw.wickets_taken) AS Wickets,
            COUNT(bw.bowling_id) AS Spells,
            ROUND(SUM(bw.overs_bowled), 1) AS Total_Overs,
            ROUND(CAST(SUM(bw.runs_conceded) AS REAL) / NULLIF(SUM(bw.overs_bowled), 0), 2) AS Economy,
            ROUND(CAST(SUM(bw.runs_conceded) AS REAL) / NULLIF(SUM(bw.wickets_taken), 0), 2) AS Bowling_Avg
        FROM bowling_scorecards bw
        JOIN players p ON bw.player_id = p.player_id
        JOIN teams t ON p.team_id = t.team_id
        JOIN matches m ON bw.match_id = m.match_id
        {format_clause}
        GROUP BY p.player_id, p.full_name, t.team_short_name
        ORDER BY Wickets DESC
        LIMIT 10;
    """
    df_wickets = execute_query(sql_wickets, format_param)
    if not df_wickets.empty:
        col_tbl, col_chart = st.columns([6, 5])
        with col_tbl:
            st.dataframe(df_wickets, hide_index=True, use_container_width=True)
        with col_chart:
            fig_wkts = px.bar(
                df_wickets,
                x="Wickets",
                y="Bowler",
                orientation="h",
                color="Economy",
                color_continuous_scale="Reds_r",
                title="Wickets Taken & Bowling Economy",
                labels={"Wickets": "Total Wickets Taken"}
            )
            fig_wkts.update_layout(**get_plotly_layout())
            fig_wkts.update_layout(yaxis={'categoryorder': 'total ascending'}, height=380)
            st.plotly_chart(fig_wkts, use_container_width=True)
    else:
        st.info("No records found for the selected filter.")

# 3. Power Hitters
with tab_power:
    st.markdown(f"#### 💥 Power Hitters — Strike Rate Benchmark • {format_filter}")
    sql_power = f"""
        SELECT 
            p.full_name AS Player,
            SUM(b.runs_scored) AS Runs,
            SUM(b.balls_faced) AS Balls,
            ROUND((CAST(SUM(b.runs_scored) AS REAL) / NULLIF(SUM(b.balls_faced), 0)) * 100.0, 2) AS Overall_SR,
            SUM(b.sixes) AS Sixes,
            SUM(b.fours) AS Fours
        FROM batting_scorecards b
        JOIN players p ON b.player_id = p.player_id
        JOIN matches m ON b.match_id = m.match_id
        {format_clause}
        GROUP BY p.player_id, p.full_name
        HAVING Balls >= 30
        ORDER BY Overall_SR DESC
        LIMIT 10;
    """
    df_power = execute_query(sql_power, format_param)
    if not df_power.empty:
        col_tbl, col_chart = st.columns([6, 5])
        with col_tbl:
            st.dataframe(df_power, hide_index=True, use_container_width=True)
        with col_chart:
            fig_power = px.scatter(
                df_power,
                x="Balls",
                y="Overall_SR",
                size="Runs",
                color="Sixes",
                hover_name="Player",
                title="Strike Rate vs Balls Faced",
                labels={"Overall_SR": "Strike Rate"},
                color_continuous_scale="Viridis"
            )
            fig_power.update_layout(**get_plotly_layout())
            fig_power.update_layout(height=380)
            st.plotly_chart(fig_power, use_container_width=True)
    else:
        st.info("No power hitters meeting minimum threshold (>= 30 balls).")

# 4. Highest Individual Innings
with tab_high:
    st.markdown(f"#### ⭐ Top 10 Highest Individual Scores • {format_filter}")
    sql_high = f"""
        SELECT 
            p.full_name AS Player,
            b.runs_scored AS Runs,
            b.balls_faced AS Balls,
            b.strike_rate AS SR,
            b.fours AS Fours,
            b.sixes AS Sixes,
            m.match_format AS Format,
            m.match_description AS Match,
            m.match_date AS Date
        FROM batting_scorecards b
        JOIN players p ON b.player_id = p.player_id
        JOIN matches m ON b.match_id = m.match_id
        {format_clause}
        ORDER BY b.runs_scored DESC
        LIMIT 10;
    """
    df_high = execute_query(sql_high, format_param)
    st.dataframe(df_high, hide_index=True, use_container_width=True)

# 5. Record Partnerships
with tab_parts:
    st.markdown("#### 🤝 Top Batting Partnerships")
    sql_parts = """
        SELECT 
            p1.full_name AS Batter_1,
            p2.full_name AS Batter_2,
            pr.partnership_runs AS Stand_Runs,
            pr.balls_faced AS Balls,
            pr.innings AS Innings,
            m.match_description AS Match
        FROM partnerships pr
        JOIN players p1 ON pr.player1_id = p1.player_id
        JOIN players p2 ON pr.player2_id = p2.player_id
        JOIN matches m ON pr.match_id = m.match_id
        ORDER BY pr.partnership_runs DESC
        LIMIT 10;
    """
    df_parts = execute_query(sql_parts)
    st.dataframe(df_parts, hide_index=True, use_container_width=True)
