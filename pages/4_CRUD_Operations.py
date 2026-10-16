"""
Cricbuzz LiveStats - Administrative Data Governance & CRUD Operations
"""

import os
import sys
import streamlit as st
import pandas as pd

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.player_service import PlayerService
from utils.ui_theme import apply_theme, render_hero

st.set_page_config(page_title="CRUD Operations | Cricbuzz LiveStats", page_icon="🛠️", layout="wide")
apply_theme()

render_hero(
    title="🛠️ Administrative Data Governance & CRUD",
    subtitle="Transactional Create, Read, Update, and Delete suite with foreign key safeguards",
    badge_text="DATA GOVERNANCE"
)

# Fetch teams for dropdowns
teams = PlayerService.get_all_teams()
team_map = {t["team_name"]: t["team_id"] for t in teams}
team_names = list(team_map.keys())

tab_read, tab_create, tab_update, tab_delete = st.tabs([
    "📋 Search & View Roster (Read)",
    "➕ Register Player (Create)",
    "✏️ Edit Player Profile (Update)",
    "🗑️ Deactivate Player (Delete)"
])

# -------------------------------------------------------------
# 1. READ / SEARCH TAB
# -------------------------------------------------------------
with tab_read:
    st.markdown("#### 📋 Player Registry & Live Search")
    
    col_s1, col_s2, col_s3 = st.columns([4, 3, 3])
    with col_s1:
        search_query = st.text_input("🔍 Search by Name", placeholder="e.g. Kohli, Rohit, Cummins...")
    with col_s2:
        filter_team = st.selectbox("Filter Team", ["All Teams"] + team_names)
    with col_s3:
        filter_role = st.selectbox("Filter Role", ["All", "Batsman", "Bowler", "All-rounder", "Wicket-keeper"])

    team_id_arg = team_map.get(filter_team) if filter_team != "All Teams" else None
    players_df = PlayerService.get_players_df(
        search_name=search_query,
        team_id=team_id_arg,
        role=filter_role,
        active_only=False
    )

    st.caption(f"Displaying **{len(players_df)}** registered players in the database.")
    st.dataframe(players_df, use_container_width=True, hide_index=True)

    csv = players_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 Export Complete Roster to CSV",
        data=csv,
        file_name="cricbuzz_players_roster.csv",
        mime="text/csv"
    )

# -------------------------------------------------------------
# 2. CREATE TAB
# -------------------------------------------------------------
with tab_create:
    st.markdown("#### ➕ Register a New International Player")
    with st.form("create_player_form", clear_on_submit=True):
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            new_name = st.text_input("Full Name *", placeholder="e.g. Yashasvi Jaiswal")
            new_team = st.selectbox("National Team *", team_names)
            new_country = st.text_input("Country Representation *", value="India")
        with col_c2:
            new_role = st.selectbox("Playing Role *", ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"])
            new_bat_style = st.selectbox("Batting Style", [
                "Right-hand bat", "Left-hand bat"
            ])
            new_bowl_style = st.selectbox("Bowling Style", [
                "Right-arm fast", "Right-arm fast-medium", "Right-arm medium",
                "Left-arm fast", "Left-arm fast-medium", "Right-arm offbreak",
                "Right-arm legbreak", "Slow left-arm orthodox", "None"
            ])

        submitted = st.form_submit_button("➕ Save Record to Database", type="primary")
        if submitted:
            try:
                new_id = PlayerService.create_player(
                    full_name=new_name,
                    team_id=team_map[new_team],
                    country=new_country,
                    playing_role=new_role,
                    batting_style=new_bat_style,
                    bowling_style=new_bowl_style
                )
                st.success(f"Player **{new_name}** registered successfully! Generated Player ID: `#{new_id}`")
            except Exception as e:
                st.error(f"Validation Error: {e}")

# -------------------------------------------------------------
# 3. UPDATE TAB
# -------------------------------------------------------------
with tab_update:
    st.markdown("#### ✏️ Modify Existing Player Profile")
    
    all_players_df = PlayerService.get_players_df(active_only=False)
    if not all_players_df.empty:
        player_choices = {
            f"#{r['player_id']} - {r['full_name']} ({r['team_name']})": r['player_id']
            for _, r in all_players_df.iterrows()
        }
        chosen_label = st.selectbox("Select Player to Edit", list(player_choices.keys()))
        chosen_pid = player_choices[chosen_label]
        player_data = PlayerService.get_player_by_id(chosen_pid)

        if player_data:
            with st.form("edit_player_form"):
                col_u1, col_u2 = st.columns(2)
                with col_u1:
                    u_name = st.text_input("Full Name", value=player_data["full_name"])
                    current_team_id = player_data["team_id"]
                    current_team_name = next((t["team_name"] for t in teams if t["team_id"] == current_team_id), team_names[0])
                    u_team = st.selectbox("National Team", team_names, index=team_names.index(current_team_name))
                    u_country = st.text_input("Country", value=player_data["country"])
                with col_u2:
                    roles_list = ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"]
                    u_role = st.selectbox("Playing Role", roles_list, index=roles_list.index(player_data["playing_role"]))
                    u_bat = st.selectbox("Batting Style", ["Right-hand bat", "Left-hand bat"], 
                                         index=0 if "Right" in player_data["batting_style"] else 1)
                    u_bowl = st.text_input("Bowling Style", value=player_data["bowling_style"])
                    u_active = st.checkbox("Active Playing Status", value=bool(player_data["is_active"]))

                update_btn = st.form_submit_button("💾 Commit Profile Updates", type="primary")
                if update_btn:
                    try:
                        PlayerService.update_player(
                            player_id=chosen_pid,
                            full_name=u_name,
                            team_id=team_map[u_team],
                            country=u_country,
                            playing_role=u_role,
                            batting_style=u_bat,
                            bowling_style=u_bowl,
                            is_active=1 if u_active else 0
                        )
                        st.success(f"Profile for **{u_name}** updated and committed to database!")
                    except Exception as e:
                        st.error(f"Update failed: {e}")
    else:
        st.info("No players currently in database.")

# -------------------------------------------------------------
# 4. DELETE TAB
# -------------------------------------------------------------
with tab_delete:
    st.markdown("#### 🗑️ Deactivate or Delete Player")
    st.warning("⚠️ **Relational Safeguard:** Deleting a player with match records will automatically trigger a **Soft Delete** (marking inactive) to protect historical scorecards.")

    if not all_players_df.empty:
        del_label = st.selectbox("Select Player to Delete", list(player_choices.keys()), key="del_selector")
        del_pid = player_choices[del_label]
        
        force_hard_delete = st.checkbox("Force Hard Delete (Permitted strictly if player has 0 historical matches)")

        if st.button("🗑️ Proceed with Deletion", type="primary"):
            try:
                res = PlayerService.delete_player(del_pid, force=force_hard_delete)
                if res["action"] == "soft_deleted":
                    st.info(f"ℹ️ {res['message']}")
                else:
                    st.success(f"✅ {res['message']}")
            except Exception as e:
                st.error(f"Deletion failed: {e}")
    else:
        st.info("No players available to delete.")
