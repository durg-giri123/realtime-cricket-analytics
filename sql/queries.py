"""
Master Catalog of 25 Enterprise SQL Analytical Queries for Cricbuzz LiveStats.
Categorized into:
- Beginner Level (Questions 1 - 8)
- Intermediate Level (Questions 9 - 16)
- Advanced Level (Questions 17 - 25)
"""

from typing import Dict, Any, List

QUERY_CATALOG: Dict[int, Dict[str, Any]] = {
    1: {
        "title": "Indian National Players Roster",
        "level": "Beginner",
        "question": "Find all players who represent India. Display their full name, playing role, batting style, and bowling style.",
        "tables": ["players", "teams"],
        "concepts": "SELECT, WHERE, INNER JOIN, ORDER BY",
        "chart_type": "table",
        "sql": """
SELECT 
    p.full_name,
    p.playing_role,
    p.batting_style,
    p.bowling_style
FROM players p
JOIN teams t ON p.team_id = t.team_id
WHERE t.team_name = 'India' OR p.country = 'India'
ORDER BY p.full_name ASC;
"""
    },
    2: {
        "title": "Matches Played in Last 30 Days",
        "level": "Beginner",
        "question": "Show all cricket matches that were played in the last 30 days. Include match description, both team names, venue name with city, and match date. Sort by most recent first.",
        "tables": ["matches", "teams", "venues"],
        "concepts": "Date filtering, Multiple Table Joins, String Concatenation",
        "chart_type": "table",
        "sql": """
SELECT 
    m.match_description,
    t1.team_name AS team_1,
    t2.team_name AS team_2,
    v.venue_name || ', ' || v.city AS venue_with_city,
    m.match_date
FROM matches m
JOIN teams t1 ON m.team1_id = t1.team_id
JOIN teams t2 ON m.team2_id = t2.team_id
JOIN venues v ON m.venue_id = v.venue_id
WHERE m.match_date >= date('now', '-30 days')
ORDER BY m.match_date DESC;
"""
    },
    3: {
        "title": "Top 10 Highest Run Scorers in ODI Cricket",
        "level": "Beginner",
        "question": "List the top 10 highest run scorers in ODI cricket. Show player name, total runs scored, batting average, and number of centuries. Display the highest run scorer first.",
        "tables": ["batting_scorecards", "players", "matches"],
        "concepts": "SUM, COUNT, Conditional Aggregation, GROUP BY, LIMIT",
        "chart_type": "bar",
        "chart_x": "player_name",
        "chart_y": "total_runs",
        "sql": """
SELECT 
    p.full_name AS player_name,
    SUM(b.runs_scored) AS total_runs,
    ROUND(CAST(SUM(b.runs_scored) AS REAL) / NULLIF(COUNT(CASE WHEN b.dismissal_status != 'not out' THEN 1 END), 0), 2) AS batting_average,
    SUM(CASE WHEN b.runs_scored >= 100 THEN 1 ELSE 0 END) AS centuries
FROM batting_scorecards b
JOIN players p ON b.player_id = p.player_id
JOIN matches m ON b.match_id = m.match_id
WHERE m.match_format = 'ODI'
GROUP BY p.player_id, p.full_name
ORDER BY total_runs DESC
LIMIT 10;
"""
    },
    4: {
        "title": "Major Cricket Venues (> 50,000 Capacity)",
        "level": "Beginner",
        "question": "Display all cricket venues that have a seating capacity of more than 50,000 spectators. Show venue name, city, country, and capacity. Order by largest capacity first.",
        "tables": ["venues"],
        "concepts": "Numerical Comparison, ORDER BY DESC",
        "chart_type": "bar",
        "chart_x": "venue_name",
        "chart_y": "capacity",
        "sql": """
SELECT 
    venue_name,
    city,
    country,
    capacity
FROM venues
WHERE capacity > 50000
ORDER BY capacity DESC;
"""
    },
    5: {
        "title": "Match Wins by Team",
        "level": "Beginner",
        "question": "Calculate how many matches each team has won. Show team name and total number of wins. Display teams with most wins first.",
        "tables": ["teams", "matches"],
        "concepts": "LEFT JOIN, COUNT, GROUP BY, Aggregate Sorting",
        "chart_type": "bar",
        "chart_x": "team_name",
        "chart_y": "total_wins",
        "sql": """
SELECT 
    t.team_name,
    COUNT(m.match_id) AS total_wins
FROM teams t
LEFT JOIN matches m ON t.team_id = m.winner_team_id AND m.match_status = 'Completed'
GROUP BY t.team_id, t.team_name
ORDER BY total_wins DESC;
"""
    },
    6: {
        "title": "Player Distribution by Playing Role",
        "level": "Beginner",
        "question": "Count how many players belong to each playing role (Batsman, Bowler, All-rounder, Wicket-keeper). Show the role and count of players for each role.",
        "tables": ["players"],
        "concepts": "GROUP BY, COUNT(*), Categorical Aggregation",
        "chart_type": "pie",
        "chart_names": "playing_role",
        "chart_values": "player_count",
        "sql": """
SELECT 
    playing_role,
    COUNT(*) AS player_count
FROM players
GROUP BY playing_role
ORDER BY player_count DESC;
"""
    },
    7: {
        "title": "Highest Batting Score Across Formats",
        "level": "Beginner",
        "question": "Find the highest individual batting score achieved in each cricket format (Test, ODI, T20I). Display the format and highest score.",
        "tables": ["batting_scorecards", "matches"],
        "concepts": "MAX(), Format Grouping, Integrity validation",
        "chart_type": "bar",
        "chart_x": "match_format",
        "chart_y": "highest_individual_score",
        "sql": """
SELECT 
    m.match_format,
    MAX(b.runs_scored) AS highest_individual_score
FROM batting_scorecards b
JOIN matches m ON b.match_id = m.match_id
GROUP BY m.match_format
ORDER BY highest_individual_score DESC;
"""
    },
    8: {
        "title": "Series Commenced in 2024",
        "level": "Beginner",
        "question": "Show all cricket series that started in the year 2024. Include series name, host country, match type, start date, and total number of matches planned.",
        "tables": ["series"],
        "concepts": "Date string functions (strftime / str), Chronological Sorting",
        "chart_type": "table",
        "sql": """
SELECT 
    series_name,
    host_country,
    match_type,
    start_date,
    total_matches
FROM series
WHERE strftime('%Y', start_date) = '2024'
ORDER BY start_date ASC;
"""
    },
    9: {
        "title": "Dual-Impact All-Rounders",
        "level": "Intermediate",
        "question": "Find all-rounder players who have scored significant runs AND taken significant wickets in their career. Display player name, total runs, total wickets, and format.",
        "tables": ["players", "batting_scorecards", "bowling_scorecards", "matches"],
        "concepts": "Cross-domain Subqueries, Multi-aggregate Joins, HAVING clause",
        "chart_type": "bar",
        "chart_x": "player_name",
        "chart_y": "total_runs",
        "sql": """
SELECT 
    p.full_name AS player_name,
    m.match_format,
    COALESCE(SUM(b.runs_scored), 0) AS total_runs,
    COALESCE(bow.total_wickets, 0) AS total_wickets
FROM players p
JOIN batting_scorecards b ON p.player_id = b.player_id
JOIN matches m ON b.match_id = m.match_id
LEFT JOIN (
    SELECT bw.player_id, mw.match_format, SUM(bw.wickets_taken) AS total_wickets
    FROM bowling_scorecards bw
    JOIN matches mw ON bw.match_id = mw.match_id
    GROUP BY bw.player_id, mw.match_format
) bow ON p.player_id = bow.player_id AND m.match_format = bow.match_format
WHERE p.playing_role = 'All-rounder'
GROUP BY p.player_id, p.full_name, m.match_format, bow.total_wickets
HAVING total_runs > 50 AND total_wickets >= 1
ORDER BY total_runs DESC;
"""
    },
    10: {
        "title": "Details of Last 20 Completed Matches",
        "level": "Intermediate",
        "question": "Get details of the last 20 completed matches. Show match description, both team names, winning team, victory margin, victory type, and venue name. Display most recent matches first.",
        "tables": ["matches", "teams", "venues"],
        "concepts": "Self-referencing Joins to teams, COALESCE for No Result, Multi-join syntax",
        "chart_type": "table",
        "sql": """
SELECT 
    m.match_description,
    t1.team_name AS team_1,
    t2.team_name AS team_2,
    COALESCE(tw.team_name, 'No Result') AS winning_team,
    m.victory_margin,
    m.victory_type,
    v.venue_name
FROM matches m
JOIN teams t1 ON m.team1_id = t1.team_id
JOIN teams t2 ON m.team2_id = t2.team_id
LEFT JOIN teams tw ON m.winner_team_id = tw.team_id
JOIN venues v ON m.venue_id = v.venue_id
WHERE m.match_status = 'Completed'
ORDER BY m.match_date DESC
LIMIT 20;
"""
    },
    11: {
        "title": "Cross-Format Player Performance Comparison",
        "level": "Intermediate",
        "question": "Compare each player's performance across different cricket formats. For players who have played at least 2 different formats, show total runs in Test, ODI, and T20I, along with overall batting average.",
        "tables": ["players", "batting_scorecards", "matches"],
        "concepts": "Pivot via CASE WHEN, Conditional Aggregation, COUNT(DISTINCT)",
        "chart_type": "bar",
        "chart_x": "player_name",
        "chart_y": "overall_batting_avg",
        "sql": """
SELECT 
    p.full_name AS player_name,
    COALESCE(SUM(CASE WHEN m.match_format = 'Test' THEN b.runs_scored END), 0) AS test_runs,
    COALESCE(SUM(CASE WHEN m.match_format = 'ODI' THEN b.runs_scored END), 0) AS odi_runs,
    COALESCE(SUM(CASE WHEN m.match_format = 'T20I' THEN b.runs_scored END), 0) AS t20i_runs,
    ROUND(CAST(SUM(b.runs_scored) AS REAL) / NULLIF(COUNT(CASE WHEN b.dismissal_status != 'not out' THEN 1 END), 0), 2) AS overall_batting_avg
FROM players p
JOIN batting_scorecards b ON p.player_id = b.player_id
JOIN matches m ON b.match_id = m.match_id
GROUP BY p.player_id, p.full_name
HAVING COUNT(DISTINCT m.match_format) >= 2
ORDER BY (test_runs + odi_runs + t20i_runs) DESC;
"""
    },
    12: {
        "title": "Home vs Away Win Analysis",
        "level": "Intermediate",
        "question": "Analyze each international team's performance when playing at home versus playing away based on venue country matching team country. Count wins in both conditions.",
        "tables": ["teams", "matches", "venues"],
        "concepts": "Conditional joins, Domain geography matching, CASE WHEN counts",
        "chart_type": "bar",
        "chart_x": "team_name",
        "chart_y": "total_wins",
        "sql": """
SELECT 
    t.team_name,
    COUNT(CASE WHEN v.country = t.country AND m.winner_team_id = t.team_id THEN 1 END) AS home_wins,
    COUNT(CASE WHEN v.country != t.country AND m.winner_team_id = t.team_id THEN 1 END) AS away_wins,
    COUNT(CASE WHEN m.winner_team_id = t.team_id THEN 1 END) AS total_wins
FROM teams t
LEFT JOIN matches m ON (t.team_id = m.team1_id OR t.team_id = m.team2_id) AND m.match_status = 'Completed'
LEFT JOIN venues v ON m.venue_id = v.venue_id
GROUP BY t.team_id, t.team_name
ORDER BY total_wins DESC;
"""
    },
    13: {
        "title": "Century Batting Partnerships (Consecutive Batsmen)",
        "level": "Intermediate",
        "question": "Identify batting partnerships where two consecutive batsmen scored a combined total of 100 or more runs in the same innings. Show both player names, partnership runs, and innings.",
        "tables": ["partnerships", "players", "matches"],
        "concepts": "Consecutive position validation ABS(p1 - p2) = 1, Threshold filtering",
        "chart_type": "bar",
        "chart_x": "batsman_1",
        "chart_y": "partnership_runs",
        "sql": """
SELECT 
    p1.full_name AS batsman_1,
    p2.full_name AS batsman_2,
    pr.player1_position AS pos_1,
    pr.player2_position AS pos_2,
    pr.partnership_runs,
    pr.innings,
    m.match_description
FROM partnerships pr
JOIN players p1 ON pr.player1_id = p1.player_id
JOIN players p2 ON pr.player2_id = p2.player_id
JOIN matches m ON pr.match_id = m.match_id
WHERE ABS(pr.player1_position - pr.player2_position) = 1
  AND pr.partnership_runs >= 100
ORDER BY pr.partnership_runs DESC;
"""
    },
    14: {
        "title": "Bowler Venue Performance & Economy",
        "level": "Intermediate",
        "question": "Examine bowling performance at different venues. Calculate average economy rate, total wickets taken, and matches played at each venue for bowlers bowling at least 3 overs.",
        "tables": ["bowling_scorecards", "players", "matches", "venues"],
        "concepts": "Multi-level GROUP BY, Bowling economy calculation, HAVING filters",
        "chart_type": "bar",
        "chart_x": "bowler_name",
        "chart_y": "total_wickets",
        "sql": """
SELECT 
    p.full_name AS bowler_name,
    v.venue_name,
    COUNT(DISTINCT bw.match_id) AS matches_played,
    SUM(bw.wickets_taken) AS total_wickets,
    ROUND(AVG(bw.economy_rate), 2) AS avg_economy_rate
FROM bowling_scorecards bw
JOIN players p ON bw.player_id = p.player_id
JOIN matches m ON bw.match_id = m.match_id
JOIN venues v ON m.venue_id = v.venue_id
WHERE bw.overs_bowled >= 3.0
GROUP BY p.player_id, p.full_name, v.venue_id, v.venue_name
HAVING COUNT(DISTINCT bw.match_id) >= 1
ORDER BY total_wickets DESC;
"""
    },
    15: {
        "title": "Clutch Performers in Close Matches",
        "level": "Intermediate",
        "question": "Identify players who perform exceptionally in close matches (decided by < 50 runs or < 5 wickets). Show average runs scored, close matches played, and close matches won.",
        "tables": ["batting_scorecards", "players", "matches"],
        "concepts": "Complex WHERE condition with OR, Match Contextualization",
        "chart_type": "bar",
        "chart_x": "player_name",
        "chart_y": "avg_runs_in_close_matches",
        "sql": """
SELECT 
    p.full_name AS player_name,
    COUNT(DISTINCT m.match_id) AS close_matches_played,
    ROUND(AVG(b.runs_scored), 2) AS avg_runs_in_close_matches,
    SUM(CASE WHEN m.winner_team_id = p.team_id THEN 1 ELSE 0 END) AS close_matches_won
FROM batting_scorecards b
JOIN players p ON b.player_id = p.player_id
JOIN matches m ON b.match_id = m.match_id
WHERE (m.victory_type = 'runs' AND m.victory_margin < 50)
   OR (m.victory_type = 'wickets' AND m.victory_margin < 5)
GROUP BY p.player_id, p.full_name
ORDER BY avg_runs_in_close_matches DESC;
"""
    },
    16: {
        "title": "Year-over-Year Batting Progression",
        "level": "Intermediate",
        "question": "Track how players' batting performance changes over different years. Show each player's average runs and strike rate per year for matches since 2020.",
        "tables": ["batting_scorecards", "players", "matches"],
        "concepts": "Date extraction (strftime), Time-based Grouping, Average computation",
        "chart_type": "bar",
        "chart_x": "player_name",
        "chart_y": "avg_runs",
        "sql": """
SELECT 
    p.full_name AS player_name,
    strftime('%Y', m.match_date) AS match_year,
    COUNT(b.performance_id) AS innings_played,
    ROUND(AVG(b.runs_scored), 2) AS avg_runs,
    ROUND(AVG(b.strike_rate), 2) AS avg_strike_rate
FROM batting_scorecards b
JOIN players p ON b.player_id = p.player_id
JOIN matches m ON b.match_id = m.match_id
WHERE m.match_date >= '2020-01-01'
GROUP BY p.player_id, p.full_name, match_year
HAVING COUNT(b.performance_id) >= 1
ORDER BY p.full_name, match_year DESC;
"""
    },
    17: {
        "title": "Toss Decision Impact on Match Outcomes",
        "level": "Advanced",
        "question": "Investigate whether winning the toss gives teams an advantage in winning matches. Calculate win percentage broken down by choosing to bat first vs bowl first.",
        "tables": ["matches"],
        "concepts": "Mathematical Percentage Calculation, CASE WHEN comparison, Decision Grouping",
        "chart_type": "pie",
        "chart_names": "toss_decision",
        "chart_values": "matches_won_by_toss_winner",
        "sql": """
SELECT 
    toss_decision,
    COUNT(*) AS total_matches,
    SUM(CASE WHEN toss_winner_id = winner_team_id THEN 1 ELSE 0 END) AS matches_won_by_toss_winner,
    ROUND((CAST(SUM(CASE WHEN toss_winner_id = winner_team_id THEN 1 ELSE 0 END) AS REAL) / COUNT(*)) * 100.0, 2) AS win_percentage
FROM matches
WHERE match_status = 'Completed' AND toss_decision IS NOT NULL
GROUP BY toss_decision;
"""
    },
    18: {
        "title": "Most Economical Bowlers in Limited-Overs Cricket",
        "level": "Advanced",
        "question": "Find the most economical bowlers in limited-overs cricket (ODI and T20). Calculate overall economy rate and total wickets taken.",
        "tables": ["bowling_scorecards", "players", "matches"],
        "concepts": "Format Filtering (IN), Dynamic Aggregated Economy Rate, HAVING filters",
        "chart_type": "bar",
        "chart_x": "bowler_name",
        "chart_y": "overall_economy_rate",
        "sql": """
SELECT 
    p.full_name AS bowler_name,
    COUNT(DISTINCT bw.match_id) AS matches_bowled,
    SUM(bw.wickets_taken) AS total_wickets,
    ROUND(CAST(SUM(bw.runs_conceded) AS REAL) / NULLIF(SUM(bw.overs_bowled), 0), 2) AS overall_economy_rate
FROM bowling_scorecards bw
JOIN players p ON bw.player_id = p.player_id
JOIN matches m ON bw.match_id = m.match_id
WHERE m.match_format IN ('ODI', 'T20I')
GROUP BY p.player_id, p.full_name
HAVING matches_bowled >= 1 AND AVG(bw.overs_bowled) >= 2.0
ORDER BY overall_economy_rate ASC;
"""
    },
    19: {
        "title": "Batsmen Scoring Consistency (Standard Deviation)",
        "level": "Advanced",
        "question": "Determine which batsmen are most consistent in their scoring using average runs and standard deviation. Lower standard deviation indicates higher consistency.",
        "tables": ["batting_scorecards", "players", "matches"],
        "concepts": "Statistical Dispersion SQRT(AVG(x^2) - AVG(x)^2), Variance",
        "chart_type": "scatter",
        "chart_x": "avg_runs",
        "chart_y": "std_dev_runs",
        "sql": """
SELECT 
    p.full_name AS batsman_name,
    COUNT(b.performance_id) AS innings_count,
    ROUND(AVG(b.runs_scored), 2) AS avg_runs,
    ROUND(SQRT(AVG(b.runs_scored * b.runs_scored) - (AVG(b.runs_scored) * AVG(b.runs_scored))), 2) AS std_dev_runs
FROM batting_scorecards b
JOIN players p ON b.player_id = p.player_id
JOIN matches m ON b.match_id = m.match_id
WHERE b.balls_faced >= 10 AND m.match_date >= '2022-01-01'
GROUP BY p.player_id, p.full_name
HAVING innings_count >= 1
ORDER BY std_dev_runs ASC;
"""
    },
    20: {
        "title": "Comprehensive Format Match Count & Averages",
        "level": "Advanced",
        "question": "Analyze match counts and batting averages across Test, ODI, and T20 for each player.",
        "tables": ["players", "batting_scorecards", "matches"],
        "concepts": "Multi-conditional Pivots, Safe NULLIF Division, Complex Matrix Grouping",
        "chart_type": "bar",
        "chart_x": "player_name",
        "chart_y": "odi_avg",
        "sql": """
SELECT 
    p.full_name AS player_name,
    COUNT(DISTINCT CASE WHEN m.match_format = 'Test' THEN m.match_id END) AS test_matches,
    ROUND(CAST(SUM(CASE WHEN m.match_format = 'Test' THEN b.runs_scored ELSE 0 END) AS REAL) / 
          NULLIF(COUNT(CASE WHEN m.match_format = 'Test' AND b.dismissal_status != 'not out' THEN 1 END), 0), 2) AS test_avg,
    COUNT(DISTINCT CASE WHEN m.match_format = 'ODI' THEN m.match_id END) AS odi_matches,
    ROUND(CAST(SUM(CASE WHEN m.match_format = 'ODI' THEN b.runs_scored ELSE 0 END) AS REAL) / 
          NULLIF(COUNT(CASE WHEN m.match_format = 'ODI' AND b.dismissal_status != 'not out' THEN 1 END), 0), 2) AS odi_avg,
    COUNT(DISTINCT CASE WHEN m.match_format = 'T20I' THEN m.match_id END) AS t20i_matches,
    ROUND(CAST(SUM(CASE WHEN m.match_format = 'T20I' THEN b.runs_scored ELSE 0 END) AS REAL) / 
          NULLIF(COUNT(CASE WHEN m.match_format = 'T20I' AND b.dismissal_status != 'not out' THEN 1 END), 0), 2) AS t20i_avg
FROM players p
JOIN batting_scorecards b ON p.player_id = b.player_id
JOIN matches m ON b.match_id = m.match_id
GROUP BY p.player_id, p.full_name
HAVING COUNT(DISTINCT m.match_id) >= 1
ORDER BY (test_matches + odi_matches + t20i_matches) DESC;
"""
    },
    21: {
        "title": "Weighted Multi-Discipline Player Ranking System",
        "level": "Advanced",
        "question": "Create a comprehensive performance ranking combining batting points, bowling points, and fielding points into a single weighted score.",
        "tables": ["players", "batting_scorecards", "bowling_scorecards", "matches"],
        "concepts": "Common Table Expressions (CTEs), Multi-Metric Linear Combination Scoring",
        "chart_type": "bar",
        "chart_x": "player_name",
        "chart_y": "comprehensive_performance_score",
        "sql": """
WITH BattingStats AS (
    SELECT 
        b.player_id,
        m.match_format,
        SUM(b.runs_scored) AS total_runs,
        ROUND(CAST(SUM(b.runs_scored) AS REAL) / NULLIF(COUNT(CASE WHEN b.dismissal_status != 'not out' THEN 1 END), 0), 2) AS bat_avg,
        ROUND(AVG(b.strike_rate), 2) AS avg_sr,
        SUM(b.catches) AS total_catches,
        SUM(b.stumpings) AS total_stumpings
    FROM batting_scorecards b
    JOIN matches m ON b.match_id = m.match_id
    GROUP BY b.player_id, m.match_format
),
BowlingStats AS (
    SELECT 
        bw.player_id,
        m.match_format,
        SUM(bw.wickets_taken) AS total_wickets,
        ROUND(CAST(SUM(bw.runs_conceded) AS REAL) / NULLIF(SUM(bw.wickets_taken), 0), 2) AS bowl_avg,
        ROUND(AVG(bw.economy_rate), 2) AS avg_econ
    FROM bowling_scorecards bw
    JOIN matches m ON bw.match_id = m.match_id
    GROUP BY bw.player_id, m.match_format
)
SELECT 
    p.full_name AS player_name,
    COALESCE(bat.match_format, bowl.match_format) AS format,
    COALESCE(bat.total_runs, 0) AS runs,
    COALESCE(bowl.total_wickets, 0) AS wickets,
    ROUND(
        (COALESCE(bat.total_runs, 0) * 0.01) + 
        (COALESCE(bat.bat_avg, 25.0) * 0.5) + 
        (COALESCE(bat.avg_sr, 80.0) * 0.3) +
        (COALESCE(bowl.total_wickets, 0) * 2.0) + 
        (COALESCE((50 - bowl.bowl_avg), 0) * 0.5) + 
        (COALESCE((6 - bowl.avg_econ), 0) * 2.0) +
        (COALESCE(bat.total_catches, 0) * 3.0) + 
        (COALESCE(bat.total_stumpings, 0) * 5.0),
        2
    ) AS comprehensive_performance_score
FROM players p
LEFT JOIN BattingStats bat ON p.player_id = bat.player_id
LEFT JOIN BowlingStats bowl ON p.player_id = bowl.player_id AND bat.match_format = bowl.match_format
WHERE bat.match_format IS NOT NULL OR bowl.match_format IS NOT NULL
ORDER BY comprehensive_performance_score DESC;
"""
    },
    22: {
        "title": "Head-to-Head Team Rivalry & Win Expectancy",
        "level": "Advanced",
        "question": "Build a head-to-head match prediction analysis between teams. Calculate total encounters, wins, average victory margins, and overall win percentages.",
        "tables": ["matches", "teams"],
        "concepts": "Symmetric Pair Normalization (CASE WHEN t1 < t2), Win Expectancy %",
        "chart_type": "bar",
        "chart_x": "team_a",
        "chart_y": "total_encounters",
        "sql": """
SELECT 
    CASE WHEN t1.team_name < t2.team_name THEN t1.team_name ELSE t2.team_name END AS team_a,
    CASE WHEN t1.team_name < t2.team_name THEN t2.team_name ELSE t1.team_name END AS team_b,
    COUNT(m.match_id) AS total_encounters,
    SUM(CASE WHEN m.winner_team_id = t1.team_id THEN 1 ELSE 0 END) AS team_1_wins,
    SUM(CASE WHEN m.winner_team_id = t2.team_id THEN 1 ELSE 0 END) AS team_2_wins,
    ROUND(AVG(m.victory_margin), 1) AS avg_victory_margin,
    ROUND((CAST(SUM(CASE WHEN m.winner_team_id = t1.team_id THEN 1 ELSE 0 END) AS REAL) / COUNT(m.match_id)) * 100.0, 1) AS team_1_win_pct
FROM matches m
JOIN teams t1 ON m.team1_id = t1.team_id
JOIN teams t2 ON m.team2_id = t2.team_id
WHERE m.match_status = 'Completed'
GROUP BY team_a, team_b
HAVING total_encounters >= 1
ORDER BY total_encounters DESC;
"""
    },
    23: {
        "title": "Recent Player Form & Momentum Categorization",
        "level": "Advanced",
        "question": "Analyze recent player form over their last 10 innings. Calculate average runs in last 5 vs last 10, 50s count, consistency, and classify form as 'Excellent Form', 'Good Form', etc.",
        "tables": ["batting_scorecards", "matches", "players"],
        "concepts": "Window Functions ROW_NUMBER() OVER(), Momentum heuristics, CASE WHEN Status Classification",
        "chart_type": "bar",
        "chart_x": "player_name",
        "chart_y": "avg_last_5",
        "sql": """
WITH RankedInnings AS (
    SELECT 
        b.player_id,
        b.runs_scored,
        b.strike_rate,
        ROW_NUMBER() OVER(PARTITION BY b.player_id ORDER BY m.match_date DESC) AS rn
    FROM batting_scorecards b
    JOIN matches m ON b.match_id = m.match_id
)
SELECT 
    p.full_name AS player_name,
    COUNT(*) AS recent_innings,
    ROUND(AVG(CASE WHEN rn <= 5 THEN runs_scored END), 2) AS avg_last_5,
    ROUND(AVG(runs_scored), 2) AS avg_last_10,
    SUM(CASE WHEN runs_scored >= 50 THEN 1 ELSE 0 END) AS fifties_count,
    ROUND(SQRT(AVG(runs_scored * runs_scored) - (AVG(runs_scored) * AVG(runs_scored))), 2) AS consistency_sd,
    CASE 
        WHEN AVG(CASE WHEN rn <= 5 THEN runs_scored END) >= 50 THEN 'Excellent Form'
        WHEN AVG(CASE WHEN rn <= 5 THEN runs_scored END) >= 35 THEN 'Good Form'
        WHEN AVG(CASE WHEN rn <= 5 THEN runs_scored END) >= 20 THEN 'Average Form'
        ELSE 'Poor Form'
    END AS form_status
FROM RankedInnings r
JOIN players p ON r.player_id = p.player_id
WHERE rn <= 10
GROUP BY p.player_id, p.full_name
ORDER BY avg_last_5 DESC;
"""
    },
    24: {
        "title": "Top Batting Partnership Combinations & Success Rate",
        "level": "Advanced",
        "question": "Study batting partnerships for consecutive batsmen pairs. Calculate average runs, 50+ stands, highest stand, and success rate %.",
        "tables": ["partnerships", "players"],
        "concepts": "Relational Duo Aggregation, Success Rate Ratio, Highest Record Maxima",
        "chart_type": "bar",
        "chart_x": "batting_duo",
        "chart_y": "avg_partnership_runs",
        "sql": """
SELECT 
    p1.full_name || ' & ' || p2.full_name AS batting_duo,
    COUNT(pr.partnership_id) AS total_partnerships,
    ROUND(AVG(pr.partnership_runs), 2) AS avg_partnership_runs,
    SUM(CASE WHEN pr.partnership_runs >= 50 THEN 1 ELSE 0 END) AS above_50_count,
    MAX(pr.partnership_runs) AS highest_partnership,
    ROUND((CAST(SUM(CASE WHEN pr.partnership_runs >= 50 THEN 1 ELSE 0 END) AS REAL) / COUNT(pr.partnership_id)) * 100.0, 1) AS success_rate_pct
FROM partnerships pr
JOIN players p1 ON pr.player1_id = p1.player_id
JOIN players p2 ON pr.player2_id = p2.player_id
WHERE ABS(pr.player1_position - pr.player2_position) = 1
GROUP BY pr.player1_id, pr.player2_id
HAVING total_partnerships >= 1
ORDER BY avg_partnership_runs DESC;
"""
    },
    25: {
        "title": "Quarterly Time-Series Player Performance Evolution",
        "level": "Advanced",
        "question": "Perform a time-series analysis tracking player batting performance changes across quarters using LAG() to classify trajectory as Ascending, Declining, or Stable.",
        "tables": ["batting_scorecards", "players", "matches"],
        "concepts": "Window LAG() OVER(), Time-series Quarterly Aggregation, Trend Delta Categorization",
        "chart_type": "line",
        "chart_x": "quarter",
        "chart_y": "avg_runs",
        "chart_color": "player_name",
        "sql": """
WITH QuarterlyStats AS (
    SELECT 
        p.player_id,
        p.full_name AS player_name,
        strftime('%Y', m.match_date) || '-Q' || ((CAST(strftime('%m', m.match_date) AS INTEGER) + 2) / 3) AS quarter,
        COUNT(b.performance_id) AS matches_count,
        ROUND(AVG(b.runs_scored), 2) AS avg_runs,
        ROUND(AVG(b.strike_rate), 2) AS avg_sr
    FROM batting_scorecards b
    JOIN players p ON b.player_id = p.player_id
    JOIN matches m ON b.match_id = m.match_id
    GROUP BY p.player_id, p.full_name, quarter
),
Trajectory AS (
    SELECT 
        player_name,
        quarter,
        avg_runs,
        avg_sr,
        LAG(avg_runs) OVER(PARTITION BY player_name ORDER BY quarter ASC) AS prev_quarter_runs
    FROM QuarterlyStats
)
SELECT 
    player_name,
    quarter,
    avg_runs,
    COALESCE(prev_quarter_runs, avg_runs) AS prev_quarter_runs,
    ROUND(avg_runs - COALESCE(prev_quarter_runs, avg_runs), 2) AS run_trend_delta,
    CASE 
        WHEN prev_quarter_runs IS NULL THEN 'Career Baseline'
        WHEN avg_runs > prev_quarter_runs + 5 THEN 'Career Ascending'
        WHEN avg_runs < prev_quarter_runs - 5 THEN 'Career Declining'
        ELSE 'Career Stable'
    END AS career_trajectory
FROM Trajectory
ORDER BY player_name, quarter ASC;
"""
    }
}
