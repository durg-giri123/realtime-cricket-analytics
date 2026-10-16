"""
Cricbuzz LiveStats - 25 Enterprise SQL Analytics Case Studies & Interactive Runner
"""

import os
import sys
import time
import streamlit as st
import pandas as pd
import plotly.express as px

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db_connection import execute_query
from utils.ui_theme import apply_theme, render_hero, get_plotly_layout
from sql.queries import QUERY_CATALOG

st.set_page_config(page_title="SQL Analytics | Cricbuzz LiveStats", page_icon="🔬", layout="wide")
apply_theme()

render_hero(
    title="🔬 25 Enterprise SQL Analytics Case Studies",
    subtitle="Interactive execution engine across Beginner, Intermediate, and Advanced problem statements",
    badge_text="25 QUERIES"
)

main_tab1, main_tab2 = st.tabs(["📚 25 Case Study Queries", "💻 Interactive SQL Sandbox"])

with main_tab1:
    # Sidebar Filters for Query Selection
    st.sidebar.markdown("### 🗂️ Query Catalog Filter")
    level_filter = st.sidebar.radio(
        "Select Difficulty Tier",
        ["All Levels (1 - 25)", "Beginner (Q1 - Q8)", "Intermediate (Q9 - Q16)", "Advanced (Q17 - Q25)"]
    )

    # Filter dictionary based on level
    if "Beginner" in level_filter:
        filtered_catalog = {k: v for k, v in QUERY_CATALOG.items() if v["level"] == "Beginner"}
    elif "Intermediate" in level_filter:
        filtered_catalog = {k: v for k, v in QUERY_CATALOG.items() if v["level"] == "Intermediate"}
    elif "Advanced" in level_filter:
        filtered_catalog = {k: v for k, v in QUERY_CATALOG.items() if v["level"] == "Advanced"}
    else:
        filtered_catalog = QUERY_CATALOG

    query_options = [f"Q{k:02d}: {v['title']} ({v['level']})" for k, v in filtered_catalog.items()]
    selected_option = st.selectbox("Choose Case Study Question", query_options)

    # Extract chosen question ID
    chosen_qid = int(selected_option.split(":")[0].replace("Q", "").strip())
    q_data = QUERY_CATALOG[chosen_qid]

    # Render Question Metadata Card
    level_pill_class = "test" if q_data['level'] == "Beginner" else "odi" if q_data['level'] == "Intermediate" else "t20"
    
    st.markdown(f"""
    <div class="match-card" style="margin-top: 10px;">
        <div class="match-header">
            <span class="series-title">
                <b>Question #{chosen_qid}: {q_data['title']}</b>
            </span>
            <span class="format-pill {level_pill_class}">{q_data['level']}</span>
        </div>
        <div style="font-size: 1.05rem; font-weight: 600; color: #F1F5F9; line-height: 1.5; margin-bottom: 14px;">
            {q_data['question']}
        </div>
        <div style="display: flex; gap: 20px; font-size: 0.85rem; color: #94A3B8; flex-wrap: wrap;">
            <span>📋 <b>Tables:</b> <code>{', '.join(q_data['tables'])}</code></span>
            <span>💡 <b>Concepts:</b> <i>{q_data['concepts']}</i></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Execution Controls
    col_btn, col_time = st.columns([2, 10])
    with col_btn:
        run_clicked = st.button("▶️ Execute Query", key=f"run_q_{chosen_qid}", type="primary")

    start_time = time.perf_counter()
    try:
        results_df = execute_query(q_data["sql"])
        exec_ms = (time.perf_counter() - start_time) * 1000.0
        success = True
    except Exception as e:
        results_df = pd.DataFrame()
        exec_ms = 0.0
        success = False
        st.error(f"Execution Error: {e}")

    if success:
        st.caption(f"⚡ Latency: **{exec_ms:.2f} ms** | Rows Returned: **{len(results_df)}** | Engine: `SQLite 3NF`")

        # Layout: Table + Visualization
        if not results_df.empty:
            tab_data, tab_vis = st.tabs(["📋 Result Dataset", "📊 Data Visualization"])
            
            with tab_data:
                st.dataframe(results_df, use_container_width=True, hide_index=True)
                csv = results_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Export Query Results to CSV",
                    data=csv,
                    file_name=f"cricbuzz_query_{chosen_qid}.csv",
                    mime="text/csv"
                )

            with tab_vis:
                chart_type = q_data.get("chart_type", "table")
                if chart_type == "bar":
                    x_col = q_data.get("chart_x")
                    y_col = q_data.get("chart_y")
                    if x_col in results_df.columns and y_col in results_df.columns:
                        fig = px.bar(
                            results_df,
                            x=x_col,
                            y=y_col,
                            color=y_col,
                            title=q_data['title'],
                            color_continuous_scale="Teal"
                        )
                        fig.update_layout(**get_plotly_layout())
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("Chart mapping not applicable for this result format.")
                elif chart_type == "pie":
                    names_col = q_data.get("chart_names")
                    values_col = q_data.get("chart_values")
                    if names_col in results_df.columns and values_col in results_df.columns:
                        fig = px.pie(
                            results_df,
                            names=names_col,
                            values=values_col,
                            title=q_data['title'],
                            hole=0.45
                        )
                        fig.update_layout(**get_plotly_layout())
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("Chart mapping not applicable for this result format.")
                elif chart_type == "line":
                    x_col = q_data.get("chart_x")
                    y_col = q_data.get("chart_y")
                    color_col = q_data.get("chart_color")
                    if x_col in results_df.columns and y_col in results_df.columns:
                        fig = px.line(
                            results_df,
                            x=x_col,
                            y=y_col,
                            color=color_col if color_col in results_df.columns else None,
                            markers=True,
                            title=q_data['title']
                        )
                        fig.update_layout(**get_plotly_layout())
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)
                elif chart_type == "scatter":
                    x_col = q_data.get("chart_x")
                    y_col = q_data.get("chart_y")
                    if x_col in results_df.columns and y_col in results_df.columns:
                        fig = px.scatter(
                            results_df,
                            x=x_col,
                            y=y_col,
                            hover_name=results_df.columns[0],
                            size_max=15,
                            title=q_data['title'],
                            color=y_col,
                            color_continuous_scale="Viridis"
                        )
                        fig.update_layout(**get_plotly_layout())
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Tabular representation is optimal for this multi-dimensional result.")
        else:
            st.warning("Query returned zero rows on the current database.")

        # Collapsible SQL Code view
        with st.expander("💻 View SQL Source Code & Optimization Strategy"):
            st.code(q_data["sql"].strip(), language="sql")

with main_tab2:
    st.markdown("#### 💻 Interactive SQL Sandbox")
    st.caption("Write and execute custom `SELECT` statements directly against the live database.")

    default_sandbox_sql = """SELECT 
    t.team_name,
    COUNT(p.player_id) AS squad_size,
    COUNT(CASE WHEN p.playing_role = 'All-rounder' THEN 1 END) AS all_rounders
FROM teams t
LEFT JOIN players p ON t.team_id = p.team_id
GROUP BY t.team_id, t.team_name
ORDER BY squad_size DESC;"""

    custom_sql = st.text_area("SQL Editor", value=default_sandbox_sql, height=180)

    if st.button("🚀 Execute Custom Query", type="primary"):
        # Basic security guard
        disallowed = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE"]
        if any(word in custom_sql.upper().split() for word in disallowed):
            st.error("Sandbox mode is read-only. Modification statements (DROP, DELETE, UPDATE, INSERT) are restricted.")
        else:
            try:
                c_start = time.perf_counter()
                custom_df = execute_query(custom_sql)
                c_ms = (time.perf_counter() - c_start) * 1000.0
                st.success(f"Executed in {c_ms:.2f} ms • {len(custom_df)} rows returned.")
                st.dataframe(custom_df, use_container_width=True, hide_index=True)
            except Exception as exc:
                st.error(f"SQL Syntax Error: {exc}")
