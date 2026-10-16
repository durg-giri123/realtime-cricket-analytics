-- ====================================================================
-- Cricbuzz LiveStats: Relational Database Schema (3NF Normalized)
-- Engine: SQLite / PostgreSQL / MySQL Compatible DDL
-- ====================================================================

PRAGMA foreign_keys = ON;

-- 1. Venues Table
CREATE TABLE IF NOT EXISTS venues (
    venue_id INTEGER PRIMARY KEY AUTOINCREMENT,
    venue_name VARCHAR(150) NOT NULL,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    capacity INTEGER CHECK (capacity >= 0)
);

-- 2. Teams Table
CREATE TABLE IF NOT EXISTS teams (
    team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name VARCHAR(100) NOT NULL UNIQUE,
    team_short_name VARCHAR(10) NOT NULL,
    country VARCHAR(100) NOT NULL
);

-- 3. Series / Tournaments Table
CREATE TABLE IF NOT EXISTS series (
    series_id INTEGER PRIMARY KEY AUTOINCREMENT,
    series_name VARCHAR(200) NOT NULL,
    host_country VARCHAR(100) NOT NULL,
    match_type VARCHAR(20) NOT NULL CHECK (match_type IN ('Test', 'ODI', 'T20I', 'Domestic')),
    start_date DATE NOT NULL,
    end_date DATE,
    total_matches INTEGER DEFAULT 1
);

-- 4. Players Table
CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name VARCHAR(120) NOT NULL,
    team_id INTEGER NOT NULL,
    country VARCHAR(100) NOT NULL,
    playing_role VARCHAR(50) NOT NULL CHECK (playing_role IN ('Batsman', 'Bowler', 'All-rounder', 'Wicket-keeper')),
    batting_style VARCHAR(50) DEFAULT 'Right-hand bat',
    bowling_style VARCHAR(50) DEFAULT 'Right-arm medium',
    is_active INTEGER DEFAULT 1 CHECK (is_active IN (0, 1)),
    FOREIGN KEY (team_id) REFERENCES teams(team_id) ON DELETE CASCADE
);

-- 5. Matches Table
CREATE TABLE IF NOT EXISTS matches (
    match_id INTEGER PRIMARY KEY AUTOINCREMENT,
    series_id INTEGER,
    match_description VARCHAR(255) NOT NULL,
    match_format VARCHAR(20) NOT NULL CHECK (match_format IN ('Test', 'ODI', 'T20I')),
    match_date DATE NOT NULL,
    venue_id INTEGER NOT NULL,
    team1_id INTEGER NOT NULL,
    team2_id INTEGER NOT NULL,
    toss_winner_id INTEGER,
    toss_decision VARCHAR(10) CHECK (toss_decision IN ('bat', 'bowl', NULL)),
    match_status VARCHAR(20) DEFAULT 'Completed' CHECK (match_status IN ('Upcoming', 'Live', 'Completed', 'Abandoned')),
    winner_team_id INTEGER,
    victory_margin INTEGER DEFAULT 0,
    victory_type VARCHAR(20) CHECK (victory_type IN ('runs', 'wickets', 'tie', 'no result', NULL)),
    FOREIGN KEY (series_id) REFERENCES series(series_id) ON DELETE SET NULL,
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id) ON DELETE RESTRICT,
    FOREIGN KEY (team1_id) REFERENCES teams(team_id) ON DELETE RESTRICT,
    FOREIGN KEY (team2_id) REFERENCES teams(team_id) ON DELETE RESTRICT,
    FOREIGN KEY (toss_winner_id) REFERENCES teams(team_id) ON DELETE SET NULL,
    FOREIGN KEY (winner_team_id) REFERENCES teams(team_id) ON DELETE SET NULL
);

-- 6. Batting Scorecards Table
CREATE TABLE IF NOT EXISTS batting_scorecards (
    performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER NOT NULL,
    innings INTEGER NOT NULL CHECK (innings BETWEEN 1 AND 4),
    batting_position INTEGER CHECK (batting_position BETWEEN 1 AND 11),
    player_id INTEGER NOT NULL,
    runs_scored INTEGER NOT NULL DEFAULT 0 CHECK (runs_scored >= 0),
    balls_faced INTEGER NOT NULL DEFAULT 0 CHECK (balls_faced >= 0),
    fours INTEGER DEFAULT 0 CHECK (fours >= 0),
    sixes INTEGER DEFAULT 0 CHECK (sixes >= 0),
    strike_rate REAL GENERATED ALWAYS AS (
        CASE WHEN balls_faced > 0 THEN ROUND((CAST(runs_scored AS REAL) / balls_faced) * 100.0, 2) ELSE 0.0 END
    ) STORED,
    dismissal_status VARCHAR(50) DEFAULT 'not out',
    catches INTEGER DEFAULT 0 CHECK (catches >= 0),
    stumpings INTEGER DEFAULT 0 CHECK (stumpings >= 0),
    FOREIGN KEY (match_id) REFERENCES matches(match_id) ON DELETE CASCADE,
    FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE RESTRICT
);

-- 7. Bowling Scorecards Table
CREATE TABLE IF NOT EXISTS bowling_scorecards (
    bowling_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER NOT NULL,
    innings INTEGER NOT NULL CHECK (innings BETWEEN 1 AND 4),
    player_id INTEGER NOT NULL,
    overs_bowled REAL NOT NULL CHECK (overs_bowled >= 0),
    maidens INTEGER DEFAULT 0 CHECK (maidens >= 0),
    runs_conceded INTEGER NOT NULL CHECK (runs_conceded >= 0),
    wickets_taken INTEGER DEFAULT 0 CHECK (wickets_taken >= 0),
    economy_rate REAL GENERATED ALWAYS AS (
        CASE WHEN overs_bowled > 0 THEN ROUND(CAST(runs_conceded AS REAL) / overs_bowled, 2) ELSE 0.0 END
    ) STORED,
    FOREIGN KEY (match_id) REFERENCES matches(match_id) ON DELETE CASCADE,
    FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE RESTRICT
);

-- 8. Batting Partnerships Table
CREATE TABLE IF NOT EXISTS partnerships (
    partnership_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER NOT NULL,
    innings INTEGER NOT NULL CHECK (innings BETWEEN 1 AND 4),
    player1_id INTEGER NOT NULL,
    player2_id INTEGER NOT NULL,
    player1_position INTEGER CHECK (player1_position BETWEEN 1 AND 11),
    player2_position INTEGER CHECK (player2_position BETWEEN 1 AND 11),
    partnership_runs INTEGER NOT NULL CHECK (partnership_runs >= 0),
    balls_faced INTEGER DEFAULT 0 CHECK (balls_faced >= 0),
    FOREIGN KEY (match_id) REFERENCES matches(match_id) ON DELETE CASCADE,
    FOREIGN KEY (player1_id) REFERENCES players(player_id) ON DELETE RESTRICT,
    FOREIGN KEY (player2_id) REFERENCES players(player_id) ON DELETE RESTRICT
);

-- ====================================================================
-- High-Performance B-Tree Indexes
-- ====================================================================
CREATE INDEX IF NOT EXISTS idx_matches_date ON matches(match_date);
CREATE INDEX IF NOT EXISTS idx_matches_format ON matches(match_format);
CREATE INDEX IF NOT EXISTS idx_matches_winner ON matches(winner_team_id);
CREATE INDEX IF NOT EXISTS idx_players_team ON players(team_id);
CREATE INDEX IF NOT EXISTS idx_players_role ON players(playing_role);
CREATE INDEX IF NOT EXISTS idx_batting_player ON batting_scorecards(player_id);
CREATE INDEX IF NOT EXISTS idx_batting_match ON batting_scorecards(match_id);
CREATE INDEX IF NOT EXISTS idx_bowling_player ON bowling_scorecards(player_id);
CREATE INDEX IF NOT EXISTS idx_bowling_match ON bowling_scorecards(match_id);
CREATE INDEX IF NOT EXISTS idx_partnerships_players ON partnerships(player1_id, player2_id);
