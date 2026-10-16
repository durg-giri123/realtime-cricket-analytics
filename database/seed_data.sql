-- ====================================================================
-- Cricbuzz LiveStats: Comprehensive Realistic Seed Data
-- Designed to satisfy all 25 SQL Analytical Queries across Formats
-- ====================================================================

-- 1. Insert Venues
INSERT OR IGNORE INTO venues (venue_id, venue_name, city, country, capacity) VALUES
(1, 'Eden Gardens', 'Kolkata', 'India', 68000),
(2, 'Wankhede Stadium', 'Mumbai', 'India', 33108),
(3, 'Narendra Modi Stadium', 'Ahmedabad', 'India', 132000),
(4, 'Melbourne Cricket Ground', 'Melbourne', 'Australia', 100024),
(5, 'Sydney Cricket Ground', 'Sydney', 'Australia', 48000),
(6, 'Lord''s Cricket Ground', 'London', 'England', 31100),
(7, 'The Oval', 'London', 'England', 27500),
(8, 'Newlands Cricket Ground', 'Cape Town', 'South Africa', 25000),
(9, 'Gaddafi Stadium', 'Lahore', 'Pakistan', 27000),
(10, 'Dubai International Cricket Stadium', 'Dubai', 'United Arab Emirates', 25000);

-- 2. Insert Teams
INSERT OR IGNORE INTO teams (team_id, team_name, team_short_name, country) VALUES
(1, 'India', 'IND', 'India'),
(2, 'Australia', 'AUS', 'Australia'),
(3, 'England', 'ENG', 'England'),
(4, 'South Africa', 'SA', 'South Africa'),
(5, 'Pakistan', 'PAK', 'Pakistan'),
(6, 'New Zealand', 'NZ', 'New Zealand');

-- 3. Insert Series
INSERT OR IGNORE INTO series (series_id, series_name, host_country, match_type, start_date, end_date, total_matches) VALUES
(1, 'Border-Gavaskar Trophy 2024', 'Australia', 'Test', '2024-11-22', '2025-01-07', 5),
(2, 'ICC Men''s T20 World Cup 2024', 'United States', 'T20I', '2024-06-01', '2024-06-29', 55),
(3, 'England Tour of India 2024', 'India', 'Test', '2024-01-25', '2024-03-11', 5),
(4, 'ICC Cricket World Cup 2023', 'India', 'ODI', '2023-10-05', '2023-11-19', 48),
(5, 'India vs South Africa Series 2023', 'South Africa', 'T20I', '2023-12-10', '2023-12-21', 3),
(6, 'Australia Tour of England 2024', 'England', 'ODI', '2024-09-19', '2024-09-29', 5);

-- 4. Insert Players
INSERT OR IGNORE INTO players (player_id, full_name, team_id, country, playing_role, batting_style, bowling_style, is_active) VALUES
(1, 'Virat Kohli', 1, 'India', 'Batsman', 'Right-hand bat', 'Right-arm medium', 1),
(2, 'Rohit Sharma', 1, 'India', 'Batsman', 'Right-hand bat', 'Right-arm offbreak', 1),
(3, 'Jasprit Bumrah', 1, 'India', 'Bowler', 'Right-hand bat', 'Right-arm fast', 1),
(4, 'Ravindra Jadeja', 1, 'India', 'All-rounder', 'Left-hand bat', 'Slow left-arm orthodox', 1),
(5, 'Rishabh Pant', 1, 'India', 'Wicket-keeper', 'Left-hand bat', 'Right-arm medium', 1),
(6, 'Hardik Pandya', 1, 'India', 'All-rounder', 'Right-hand bat', 'Right-arm fast-medium', 1),
(7, 'Shubman Gill', 1, 'India', 'Batsman', 'Right-hand bat', 'Right-arm offbreak', 1),
(8, 'Steve Smith', 2, 'Australia', 'Batsman', 'Right-hand bat', 'Right-arm legbreak', 1),
(9, 'Pat Cummins', 2, 'Australia', 'Bowler', 'Right-hand bat', 'Right-arm fast', 1),
(10, 'Glenn Maxwell', 2, 'Australia', 'All-rounder', 'Right-hand bat', 'Right-arm offbreak', 1),
(11, 'Travis Head', 2, 'Australia', 'Batsman', 'Left-hand bat', 'Right-arm offbreak', 1),
(12, 'Mitchell Starc', 2, 'Australia', 'Bowler', 'Left-hand bat', 'Left-arm fast', 1),
(13, 'Joe Root', 3, 'England', 'Batsman', 'Right-hand bat', 'Right-arm offbreak', 1),
(14, 'Ben Stokes', 3, 'England', 'All-rounder', 'Left-hand bat', 'Right-arm fast-medium', 1),
(15, 'Jos Buttler', 3, 'England', 'Wicket-keeper', 'Right-hand bat', 'Right-arm medium', 1),
(16, 'Jofra Archer', 3, 'England', 'Bowler', 'Right-hand bat', 'Right-arm fast', 1),
(17, 'Heinrich Klaasen', 4, 'South Africa', 'Wicket-keeper', 'Right-hand bat', 'Right-arm offbreak', 1),
(18, 'Kagiso Rabada', 4, 'South Africa', 'Bowler', 'Left-hand bat', 'Right-arm fast', 1),
(19, 'Babar Azam', 5, 'Pakistan', 'Batsman', 'Right-hand bat', 'Right-arm offbreak', 1),
(20, 'Shaheen Afridi', 5, 'Pakistan', 'Bowler', 'Left-hand bat', 'Left-arm fast', 1),
(21, 'Kane Williamson', 6, 'New Zealand', 'Batsman', 'Right-hand bat', 'Right-arm offbreak', 1),
(22, 'Trent Boult', 6, 'New Zealand', 'Bowler', 'Right-hand bat', 'Left-arm fast-medium', 1);

-- 5. Insert Matches (spanning recent dates, formats, toss outcomes, margins)
INSERT OR IGNORE INTO matches (match_id, series_id, match_description, match_format, match_date, venue_id, team1_id, team2_id, toss_winner_id, toss_decision, match_status, winner_team_id, victory_margin, victory_type) VALUES
-- Matches within last 30 days
(1, 1, '1st Test - Australia vs India', 'Test', date('now', '-5 days'), 4, 2, 1, 1, 'bat', 'Completed', 1, 295, 'runs'),
(2, 6, '5th ODI - England vs Australia', 'ODI', date('now', '-12 days'), 6, 3, 2, 2, 'bowl', 'Completed', 2, 49, 'runs'),
(3, 2, 'T20I Showcase - India vs South Africa', 'T20I', date('now', '-18 days'), 2, 1, 4, 1, 'bat', 'Completed', 1, 7, 'runs'),
(4, 6, '4th ODI - England vs Australia', 'ODI', date('now', '-24 days'), 7, 3, 2, 3, 'bat', 'Completed', 3, 186, 'runs'),
(5, 1, 'Warmup Match - India vs Australia XI', 'Test', date('now', '-28 days'), 5, 1, 2, 2, 'bowl', 'Completed', 1, 4, 'wickets'),

-- Historic & Tournament Matches (2023 & 2024)
(6, 4, 'World Cup Final - India vs Australia', 'ODI', '2023-11-19', 3, 1, 2, 2, 'bowl', 'Completed', 2, 6, 'wickets'),
(7, 4, 'World Cup Semi-Final - India vs New Zealand', 'ODI', '2023-11-15', 2, 1, 6, 1, 'bat', 'Completed', 1, 70, 'runs'),
(8, 2, 'T20 World Cup Final - India vs South Africa', 'T20I', '2024-06-29', 10, 1, 4, 1, 'bat', 'Completed', 1, 7, 'runs'),
(9, 3, '1st Test - India vs England', 'Test', '2024-01-28', 1, 1, 3, 3, 'bat', 'Completed', 3, 28, 'runs'),
(10, 3, '2nd Test - India vs England', 'Test', '2024-02-05', 2, 1, 3, 1, 'bat', 'Completed', 1, 106, 'runs'),
(11, 4, 'ODI League - England vs South Africa', 'ODI', '2023-10-21', 2, 3, 4, 3, 'bowl', 'Completed', 4, 229, 'runs'),
(12, 4, 'ODI League - Australia vs New Zealand', 'ODI', '2023-10-28', 3, 2, 6, 6, 'bowl', 'Completed', 2, 5, 'runs'),
(13, 2, 'T20 Group Stage - India vs Pakistan', 'T20I', '2024-06-09', 10, 1, 5, 5, 'bowl', 'Completed', 1, 6, 'runs'),
(14, 5, '2nd T20I - South Africa vs India', 'T20I', '2023-12-12', 8, 4, 1, 4, 'bowl', 'Completed', 4, 5, 'wickets'),
(15, 5, '3rd T20I - South Africa vs India', 'T20I', '2023-12-14', 8, 4, 1, 4, 'bowl', 'Completed', 1, 106, 'runs'),
(16, 4, 'ODI League - India vs Pakistan', 'ODI', '2023-10-14', 3, 1, 5, 1, 'bowl', 'Completed', 1, 7, 'wickets'),
(17, 4, 'ODI League - Australia vs England', 'ODI', '2023-11-04', 3, 2, 3, 3, 'bowl', 'Completed', 2, 33, 'runs'),
(18, 3, '3rd Test - India vs England', 'Test', '2024-02-18', 3, 1, 3, 1, 'bat', 'Completed', 1, 434, 'runs'),
(19, 4, 'ODI League - South Africa vs Pakistan', 'ODI', '2023-10-27', 1, 4, 5, 5, 'bat', 'Completed', 4, 1, 'wickets'),
(20, 2, 'T20 Semi Final - South Africa vs Afghanistan', 'T20I', '2024-06-27', 10, 4, 5, 5, 'bat', 'Completed', 4, 9, 'wickets');

-- 6. Insert Batting Scorecards
INSERT OR IGNORE INTO batting_scorecards (performance_id, match_id, innings, batting_position, player_id, runs_scored, balls_faced, fours, sixes, dismissal_status, catches, stumpings) VALUES
-- Match 1 (Test: Ind vs Aus)
(1, 1, 1, 1, 7, 38, 54, 4, 0, 'caught', 1, 0),
(2, 1, 1, 2, 2, 52, 70, 7, 1, 'bowled', 0, 0),
(3, 1, 1, 3, 1, 100, 143, 8, 2, 'not out', 2, 0),
(4, 1, 1, 4, 5, 71, 85, 8, 2, 'caught', 3, 1),
(5, 1, 1, 5, 4, 42, 60, 4, 1, 'caught', 1, 0),
(6, 1, 2, 1, 11, 40, 52, 5, 1, 'caught', 0, 0),
(7, 1, 2, 2, 8, 55, 98, 6, 0, 'lbw', 1, 0),

-- Match 2 (ODI: Eng vs Aus)
(8, 2, 1, 1, 11, 88, 76, 9, 3, 'caught', 0, 0),
(9, 2, 1, 2, 8, 65, 78, 5, 1, 'caught', 1, 0),
(10, 2, 1, 3, 10, 45, 32, 4, 3, 'bowled', 0, 0),
(11, 2, 2, 1, 13, 72, 84, 7, 0, 'caught', 0, 0),
(12, 2, 2, 2, 15, 62, 55, 6, 2, 'caught', 1, 1),

-- Match 3 (T20I: Ind vs SA - Close finish, 7 runs)
(13, 3, 1, 1, 2, 57, 39, 5, 3, 'caught', 0, 0),
(14, 3, 1, 2, 1, 76, 48, 6, 3, 'not out', 1, 0),
(15, 3, 1, 3, 6, 35, 20, 2, 2, 'run out', 0, 0),
(16, 3, 2, 1, 17, 81, 44, 7, 5, 'caught', 0, 0),

-- Match 6 (World Cup Final: Ind vs Aus)
(17, 6, 1, 1, 2, 47, 31, 4, 3, 'caught', 0, 0),
(18, 6, 1, 2, 1, 54, 63, 4, 0, 'bowled', 0, 0),
(19, 6, 2, 1, 11, 137, 120, 15, 4, 'caught', 1, 0),
(20, 6, 2, 2, 8, 44, 42, 4, 1, 'not out', 1, 0),

-- Match 7 (World Cup Semi-Final: Ind vs NZ)
(21, 7, 1, 1, 2, 47, 29, 4, 4, 'caught', 0, 0),
(22, 7, 1, 2, 7, 80, 66, 8, 3, 'retired hurt', 0, 0),
(23, 7, 1, 3, 1, 117, 113, 9, 2, 'caught', 1, 0),
(24, 7, 2, 1, 21, 69, 73, 8, 1, 'caught', 0, 0),

-- Match 8 (T20 WC Final: Ind vs SA - Close Match, 7 runs)
(25, 8, 1, 1, 1, 76, 59, 6, 2, 'caught', 1, 0),
(26, 8, 1, 2, 6, 25, 17, 2, 1, 'not out', 0, 0),
(27, 8, 2, 1, 17, 52, 27, 2, 5, 'caught', 0, 0),

-- Match 9 (Test: Ind vs Eng)
(28, 9, 1, 1, 13, 122, 180, 12, 1, 'caught', 2, 0),
(29, 9, 1, 2, 14, 70, 95, 8, 2, 'lbw', 1, 0),
(30, 9, 2, 1, 4, 87, 120, 9, 1, 'run out', 0, 0),

-- Match 12 (ODI: Aus vs NZ - Close Match, 5 runs)
(31, 12, 1, 1, 11, 109, 67, 10, 7, 'bowled', 0, 0),
(32, 12, 1, 2, 10, 41, 24, 5, 2, 'caught', 1, 0),
(33, 12, 2, 1, 21, 85, 88, 7, 1, 'caught', 0, 0),

-- Match 18 (Test: Ind vs Eng)
(34, 18, 1, 1, 2, 131, 196, 14, 3, 'caught', 0, 0),
(35, 18, 1, 2, 4, 112, 225, 9, 2, 'caught', 1, 0),
(36, 18, 2, 1, 13, 65, 90, 7, 0, 'caught', 0, 0),

-- Match 19 (ODI: SA vs Pak - Close Match, 1 wicket)
(37, 19, 1, 1, 19, 50, 65, 4, 1, 'caught', 0, 0),
(38, 19, 2, 1, 17, 36, 40, 3, 1, 'caught', 1, 0);

-- 7. Insert Bowling Scorecards
INSERT OR IGNORE INTO bowling_scorecards (bowling_id, match_id, innings, player_id, overs_bowled, maidens, runs_conceded, wickets_taken) VALUES
-- Match 1 (Test: Ind vs Aus)
(1, 1, 1, 9, 18.0, 3, 58, 3),
(2, 1, 1, 12, 16.4, 2, 65, 4),
(3, 1, 2, 3, 15.0, 4, 30, 5),
(4, 1, 2, 4, 12.0, 2, 35, 3),

-- Match 2 (ODI: Eng vs Aus)
(5, 2, 1, 14, 7.0, 0, 42, 2),
(6, 2, 1, 16, 9.0, 1, 52, 3),
(7, 2, 2, 9, 8.2, 1, 38, 3),
(8, 2, 2, 12, 9.0, 0, 45, 4),

-- Match 3 (T20I: Ind vs SA)
(9, 3, 1, 18, 4.0, 0, 32, 2),
(10, 3, 2, 3, 4.0, 0, 21, 3),
(11, 3, 2, 6, 3.0, 0, 26, 2),

-- Match 6 (World Cup Final: Ind vs Aus)
(12, 6, 1, 9, 10.0, 0, 34, 2),
(13, 6, 1, 12, 10.0, 0, 55, 3),
(14, 6, 2, 3, 9.0, 2, 43, 2),

-- Match 7 (World Cup Semi-Final: Ind vs NZ)
(15, 7, 1, 22, 10.0, 0, 86, 1),
(16, 7, 2, 3, 10.0, 1, 57, 7),

-- Match 8 (T20 WC Final: Ind vs SA)
(17, 8, 1, 18, 4.0, 0, 36, 1),
(18, 8, 2, 3, 4.0, 0, 18, 2),
(19, 8, 2, 6, 3.0, 0, 20, 3),

-- Match 9 (Test: Ind vs Eng)
(20, 9, 1, 4, 21.0, 4, 65, 3),
(21, 9, 1, 3, 18.0, 3, 41, 4),
(22, 9, 2, 14, 14.0, 2, 48, 2),

-- Match 13 (T20I: Ind vs Pak)
(23, 13, 1, 20, 4.0, 0, 29, 3),
(24, 13, 2, 3, 4.0, 0, 14, 3),
(25, 13, 2, 6, 4.0, 0, 24, 2),

-- Match 18 (Test: Ind vs Eng)
(26, 18, 1, 16, 19.0, 2, 74, 2),
(27, 18, 2, 4, 15.0, 3, 41, 5),
(28, 18, 2, 3, 12.0, 2, 32, 3);

-- 8. Insert Partnerships
INSERT OR IGNORE INTO partnerships (partnership_id, match_id, innings, player1_id, player2_id, player1_position, player2_position, partnership_runs, balls_faced) VALUES
(1, 1, 1, 2, 1, 2, 3, 114, 142),
(2, 1, 1, 1, 5, 3, 4, 108, 115),
(3, 2, 1, 11, 8, 1, 2, 122, 95),
(4, 3, 1, 2, 1, 1, 2, 105, 68),
(5, 7, 1, 7, 1, 2, 3, 163, 128),
(6, 7, 1, 1, 2, 3, 4, 128, 102),
(7, 18, 1, 2, 4, 1, 2, 204, 248),
(8, 6, 2, 11, 8, 1, 2, 192, 215),
(9, 8, 1, 1, 6, 1, 2, 67, 44),
(10, 12, 1, 11, 10, 1, 2, 85, 52);
