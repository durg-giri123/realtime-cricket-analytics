"""
Player & Match Service Layer for Cricbuzz LiveStats.
Encapsulates CRUD operations, data validation, and business logic.
"""

from typing import List, Dict, Any, Optional
import pandas as pd
from utils.db_connection import execute_query, execute_dml, get_db_connection


class PlayerService:
    """Manages player data CRUD operations and business validation rules."""

    @staticmethod
    def get_all_teams() -> List[Dict[str, Any]]:
        """Fetches all registered teams."""
        df = execute_query("SELECT team_id, team_name, team_short_name, country FROM teams ORDER BY team_name ASC;")
        return df.to_dict(orient="records")

    @staticmethod
    def get_all_venues() -> List[Dict[str, Any]]:
        """Fetches all registered venues."""
        df = execute_query("SELECT venue_id, venue_name, city, country, capacity FROM venues ORDER BY venue_name ASC;")
        return df.to_dict(orient="records")

    @staticmethod
    def get_players_df(
        search_name: Optional[str] = None,
        team_id: Optional[int] = None,
        role: Optional[str] = None,
        active_only: bool = True
    ) -> pd.DataFrame:
        """
        Retrieves players with flexible filtering by name, team, and role.
        """
        sql = """
            SELECT 
                p.player_id,
                p.full_name,
                t.team_name,
                t.team_short_name,
                p.country,
                p.playing_role,
                p.batting_style,
                p.bowling_style,
                CASE WHEN p.is_active = 1 THEN 'Active' ELSE 'Inactive' END AS status
            FROM players p
            JOIN teams t ON p.team_id = t.team_id
            WHERE 1=1
        """
        params = []
        if active_only:
            sql += " AND p.is_active = 1"
        if search_name:
            sql += " AND p.full_name LIKE ?"
            params.append(f"%{search_name.strip()}%")
        if team_id:
            sql += " AND p.team_id = ?"
            params.append(team_id)
        if role and role != "All":
            sql += " AND p.playing_role = ?"
            params.append(role)

        sql += " ORDER BY p.full_name ASC"
        return execute_query(sql, tuple(params))

    @staticmethod
    def get_player_by_id(player_id: int) -> Optional[Dict[str, Any]]:
        """Fetches a single player record by ID."""
        df = execute_query("SELECT * FROM players WHERE player_id = ?", (player_id,))
        if not df.empty:
            return df.iloc[0].to_dict()
        return None

    @staticmethod
    def create_player(
        full_name: str,
        team_id: int,
        country: str,
        playing_role: str,
        batting_style: str = "Right-hand bat",
        bowling_style: str = "Right-arm medium",
        is_active: int = 1
    ) -> int:
        """
        Validates input and inserts a new player record into the database.
        Returns the new player_id.
        """
        if not full_name or len(full_name.strip()) < 2:
            raise ValueError("Player name must be at least 2 characters long.")
        if not country or len(country.strip()) < 2:
            raise ValueError("Country must be specified.")
        valid_roles = ['Batsman', 'Bowler', 'All-rounder', 'Wicket-keeper']
        if playing_role not in valid_roles:
            raise ValueError(f"Invalid playing role. Must be one of: {', '.join(valid_roles)}")

        sql = """
            INSERT INTO players (full_name, team_id, country, playing_role, batting_style, bowling_style, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        return execute_dml(sql, (
            full_name.strip(),
            team_id,
            country.strip(),
            playing_role,
            batting_style,
            bowling_style,
            is_active
        ))

    @staticmethod
    def update_player(
        player_id: int,
        full_name: str,
        team_id: int,
        country: str,
        playing_role: str,
        batting_style: str,
        bowling_style: str,
        is_active: int
    ) -> bool:
        """Updates an existing player's details."""
        if not full_name or len(full_name.strip()) < 2:
            raise ValueError("Player name must be at least 2 characters long.")

        sql = """
            UPDATE players
            SET full_name = ?,
                team_id = ?,
                country = ?,
                playing_role = ?,
                batting_style = ?,
                bowling_style = ?,
                is_active = ?
            WHERE player_id = ?;
        """
        execute_dml(sql, (
            full_name.strip(),
            team_id,
            country.strip(),
            playing_role,
            batting_style,
            bowling_style,
            is_active,
            player_id
        ))
        return True

    @staticmethod
    def delete_player(player_id: int, force: bool = False) -> Dict[str, Any]:
        """
        Safely deletes a player. If player has existing match performances,
        performs soft delete (marks inactive) unless force is True.
        """
        # Check existing performances
        perf_check = execute_query(
            """
            SELECT 
                (SELECT COUNT(*) FROM batting_scorecards WHERE player_id = ?) +
                (SELECT COUNT(*) FROM bowling_scorecards WHERE player_id = ?) AS total_records
            """,
            (player_id, player_id)
        )
        total_records = int(perf_check.iloc[0]['total_records']) if not perf_check.empty else 0

        if total_records > 0 and not force:
            # Soft delete to preserve historical integrity
            execute_dml("UPDATE players SET is_active = 0 WHERE player_id = ?", (player_id,))
            return {
                "action": "soft_deleted",
                "message": f"Player marked inactive because they have {total_records} historical match records."
            }
        else:
            execute_dml("DELETE FROM players WHERE player_id = ?", (player_id,))
            return {
                "action": "hard_deleted",
                "message": "Player record permanently deleted from database."
            }
