# 🏏 Cricbuzz LiveStats: Real-Time Cricket Insights & SQL-Based Analytics

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://realtime-cricket-analytics-zwcckghmtjbz86d3mpkw59.streamlit.app/)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/durg-giri123/realtime-cricket-analytics)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![Database](https://img.shields.io/badge/Database-SQLite%203NF-green?logo=sqlite)](https://www.sqlite.org/)

> 🚀 **Live Application:** [https://realtime-cricket-analytics-zwcckghmtjbz86d3mpkw59.streamlit.app/](https://realtime-cricket-analytics-zwcckghmtjbz86d3mpkw59.streamlit.app/)

A comprehensive sports analytics and database management platform that integrates live cricket data from the **Cricbuzz REST API** with a **3NF-normalized relational SQL database** and an interactive multi-page **Streamlit dashboard**.

---

## 🌟 Key Features

1. **⚡ Real-Time Match Updates (`pages/1_Live_Matches.py`):**
   - Ingests ongoing cricket matches via Cricbuzz REST API (RapidAPI).
   - Real-time scorecards, overs, run rates, active batsmen, and current bowler metrics.
   - Built-in zero-downtime offline simulator fallback if API keys or rate limits expire.
   - One-click ingestion to save live match data into the SQLite database.

2. **📊 Top Player Statistics & Leaderboards (`pages/2_Top_Stats.py`):**
   - High-level aggregations across Test, ODI, and T20I formats.
   - Most runs, highest batting averages, most wickets, best bowling economy, and record partnerships.
   - Interactive Plotly visualizations (horizontal bar charts, scatter plots).

3. **🔍 25 Enterprise SQL Analytics Case Studies (`pages/3_SQL_Analytics.py`):**
   - **Beginner Level (Q1–Q8):** Filtering, grouping, multi-table joins, formatting.
   - **Intermediate Level (Q9–Q16):** Subqueries, conditional aggregates, clutch close-match analysis, venue economy.
   - **Advanced Level (Q17–Q25):** Window functions (`ROW_NUMBER`, `LAG`), CTEs, toss advantage calculation, weighted multi-discipline scoring, standard deviation consistency metrics.
   - Interactive execution, execution time measurement, CSV export, and tailored Plotly charts for each query.
   - Interactive Custom SQL Sandbox for executing ad-hoc queries safely.

4. **🛠️ Data Governance & CRUD Operations (`pages/4_CRUD_Operations.py`):**
   - Form-based administration for players and teams.
   - Complete Create, Read, Update, and Delete operations.
   - Defensive validation and automatic Soft Delete to protect foreign key relational integrity.

---

## 🏗️ Project Architecture

```
cricbuzz_livestats/
│
├── app.py                       # Main portal & orientation dashboard
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment configuration template
├── .env                         # Local environment configuration
├── README.md                    # Project documentation
│
├── database/
│   ├── schema.sql               # 3NF relational database schema DDL
│   ├── seed_data.sql            # Rich seed data for offline analytics
│   └── cricbuzz_stats.db        # SQLite relational database
│
├── services/
│   ├── api_client.py            # Cricbuzz API connector with mock fallback
│   └── player_service.py        # Business logic & CRUD service layer
│
├── sql/
│   └── queries.py               # Complete catalog of all 25 SQL queries & metadata
│
├── utils/
│   ├── db_connection.py         # Thread-safe DB context manager & query runner
│   └── ui_theme.py              # Broadcast dark sports design engine
│
└── pages/
    ├── 1_Live_Matches.py        # Real-time scorecards & match ingestion
    ├── 2_Top_Stats.py           # Player leaderboards & interactive charts
    ├── 3_SQL_Analytics.py       # 25 SQL case studies & interactive runner
    └── 4_CRUD_Operations.py     # Player & match administrative forms
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10 or higher
- Git

### 2. Installation
Clone or navigate to the project directory:
```bash
cd "c:\Users\DURGESH\OneDrive - galgotiasuniversity.edu.in\Desktop\Cricbuzz LiveStats"
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables (Optional)
Copy `.env.example` to `.env` and add your RapidAPI Key if you have one:
```ini
RAPIDAPI_KEY=your_key_here
RAPIDAPI_HOST=cricbuzz-cricket.p.rapidapi.com
DATABASE_PATH=database/cricbuzz_stats.db
```
*(Note: If no key is provided, the application automatically runs in Live Simulator mode so all features work immediately without downtime).*

### 4. Run the Streamlit Dashboard
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🧮 25 SQL Case Studies Overview

| # | Question Title | Difficulty | Core SQL Concepts |
|---|---|---|---|
| 1 | Indian National Players Roster | Beginner | `SELECT`, `WHERE`, `INNER JOIN` |
| 2 | Matches Played in Last 30 Days | Beginner | Date filtering, Multi-table joins |
| 3 | Top 10 ODI Run Scorers | Beginner | `SUM`, `COUNT`, `GROUP BY`, `LIMIT` |
| 4 | Venues Capacity > 50,000 | Beginner | Numerical filtering, `ORDER BY` |
| 5 | Match Wins by Team | Beginner | `LEFT JOIN`, `COUNT`, `GROUP BY` |
| 6 | Player Role Distribution | Beginner | `COUNT(*)`, Categorical aggregation |
| 7 | Highest Score Across Formats | Beginner | `MAX()`, Format grouping |
| 8 | Series Commenced in 2024 | Beginner | `strftime('%Y')`, Date sorting |
| 9 | Dual-Impact All-Rounders | Intermediate | Cross-domain Subqueries, `HAVING` |
| 10 | Details of Last 20 Matches | Intermediate | Self-joins, `COALESCE`, `LIMIT` |
| 11 | Cross-Format Performance | Intermediate | `CASE WHEN` Pivot, `COUNT(DISTINCT)` |
| 12 | Home vs Away Win Analysis | Intermediate | Venue vs Team Country conditional matching |
| 13 | Consecutive Century Partnerships | Intermediate | `ABS(p1 - p2) = 1`, Threshold filtering |
| 14 | Bowler Venue Performance | Intermediate | Multi-level grouping, Bowling economy |
| 15 | Clutch Close-Match Performers | Intermediate | Complex compound `WHERE`, Margin logic |
| 16 | Year-over-Year Batting Changes | Intermediate | Multi-year grouping, Averages & Strike Rates |
| 17 | Toss Decision Win Percentage | Advanced | Mathematical percentage, Outcome grouping |
| 18 | Most Economical Bowlers | Advanced | Format filtering, Dynamic aggregate economy |
| 19 | Batsmen Scoring Consistency | Advanced | Standard Deviation `SQRT(AVG(x^2) - AVG(x)^2)` |
| 20 | Multi-Format Match & Averages Matrix | Advanced | Pivoted conditional averages, `NULLIF` |
| 21 | Weighted Performance Ranking System | Advanced | Multi-metric CTEs, Linear combination points |
| 22 | Head-to-Head Prediction Analysis | Advanced | Symmetric pair grouping, Win expectancy |
| 23 | Recent Form & Momentum | Advanced | `ROW_NUMBER() OVER()`, Form classification |
| 24 | Batting Partnerships Success Rate | Advanced | Duo aggregations, 50+ conversion ratio |
| 25 | Quarterly Player Evolution Trajectory | Advanced | `LAG() OVER()`, Quarterly trend deltas |

---

## 🛡️ Coding & Engineering Standards
- **Clean Architecture:** Strict separation between Presentation (`pages/`), Business Logic (`services/`), and Persistence (`database/`).
- **PEP 8 Compliance:** Documented functions, type hints, and modular code blocks.
- **Defensive Database Design:** Parameterized queries, foreign key constraints (`PRAGMA foreign_keys = ON`), and WAL journal mode.
- **Relational Integrity:** Soft deletes to prevent orphan records or foreign key crashes.
