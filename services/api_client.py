"""
Cricbuzz REST API Client with error resilience, rate-limiting guards,
and offline mock fallbacks for local testing and zero-downtime execution.
"""

import os
import requests
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

load_dotenv()


class CricbuzzApiClient:
    """
    Client for interacting with Cricbuzz Cricket API via RapidAPI.
    Provides methods for live matches, scorecards, and player stats.
    Includes automatic graceful fallback to realistic data if API key is missing or quota is exhausted.
    """

    def __init__(self):
        self.api_key = os.getenv("RAPIDAPI_KEY", "").strip()
        self.api_host = os.getenv("RAPIDAPI_HOST", "cricbuzz-cricket.p.rapidapi.com").strip()
        self.base_url = f"https://{self.api_host}"
        self.timeout = 10  # Seconds

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": self.api_host,
            "Content-Type": "application/json",
        }

    def is_configured(self) -> bool:
        """Checks if a valid-looking API key is provided."""
        return bool(self.api_key and self.api_key != "your_rapidapi_key_here")

    def get_live_matches(self) -> List[Dict[str, Any]]:
        """
        Fetches ongoing live cricket matches.
        Falls back to realistic sample live feed if external API is unreachable.
        """
        if not self.is_configured():
            return self._get_fallback_live_matches(reason="API key not configured (using mock live feed)")

        endpoint = f"{self.base_url}/matches/v1/live"
        try:
            response = requests.get(endpoint, headers=self.headers, timeout=self.timeout)
            if response.status_code == 200:
                data = response.json()
                matches = self._normalize_matches_response(data)
                if matches:
                    return matches
            elif response.status_code in (401, 403, 429):
                return self._get_fallback_live_matches(
                    reason=f"API Quota/Auth issue (HTTP {response.status_code}) - displaying live cached matches"
                )
        except Exception as exc:
            return self._get_fallback_live_matches(reason=f"Network error: {str(exc)}")

        return self._get_fallback_live_matches(reason="Live feed offline")

    def _normalize_matches_response(self, raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Normalizes heterogeneous API response formats into a consistent structure."""
        normalized = []
        type_matches = raw_data.get("typeMatches", [])
        for tm in type_matches:
            match_type = tm.get("matchType", "International")
            series_matches = tm.get("seriesMatches", [])
            for sm in series_matches:
                series_ad = sm.get("seriesAdWrapper", {})
                matches_list = series_ad.get("matches", [])
                for m in matches_list:
                    match_info = m.get("matchInfo", {})
                    match_score = m.get("matchScore", {})
                    team1_score = match_score.get("team1Score", {}).get("inngs1", {})
                    team2_score = match_score.get("team2Score", {}).get("inngs1", {})

                    normalized.append({
                        "match_id": match_info.get("matchId"),
                        "series_name": series_ad.get("seriesName", "International Series"),
                        "match_desc": match_info.get("matchDesc", "Match"),
                        "format": match_info.get("matchFormat", "T20"),
                        "status": match_info.get("status", "Live"),
                        "venue": match_info.get("venueInfo", {}).get("ground", "Stadium"),
                        "city": match_info.get("venueInfo", {}).get("city", "City"),
                        "team1": match_info.get("team1", {}).get("teamName", "Team A"),
                        "team1_short": match_info.get("team1", {}).get("teamSName", "T1"),
                        "team1_runs": team1_score.get("runs", 0),
                        "team1_wickets": team1_score.get("wickets", 0),
                        "team1_overs": team1_score.get("overs", 0.0),
                        "team2": match_info.get("team2", {}).get("teamName", "Team B"),
                        "team2_short": match_info.get("team2", {}).get("teamSName", "T2"),
                        "team2_runs": team2_score.get("runs", 0),
                        "team2_wickets": team2_score.get("wickets", 0),
                        "team2_overs": team2_score.get("overs", 0.0),
                    })
        return normalized

    def _get_fallback_live_matches(self, reason: str = "") -> List[Dict[str, Any]]:
        """Realistic mock live match feed for local demonstration and testing."""
        return [
            {
                "match_id": 90101,
                "series_name": "Border-Gavaskar Trophy 2024-25",
                "match_desc": "1st Test - Day 3",
                "format": "Test",
                "status": "India lead by 218 runs",
                "venue": "Optus Stadium",
                "city": "Perth",
                "team1": "India",
                "team1_short": "IND",
                "team1_runs": 150,
                "team1_wickets": 10,
                "team1_overs": 49.4,
                "team2": "Australia",
                "team2_short": "AUS",
                "team2_runs": 104,
                "team2_wickets": 10,
                "team2_overs": 51.2,
                "current_batters": [
                    {"name": "Virat Kohli", "runs": 100, "balls": 143, "fours": 8, "sixes": 2, "sr": 69.93},
                    {"name": "Rishabh Pant", "runs": 71, "balls": 85, "fours": 8, "sixes": 2, "sr": 83.53}
                ],
                "current_bowler": {"name": "Pat Cummins", "overs": 18.0, "maidens": 3, "runs": 58, "wickets": 3, "economy": 3.22},
                "partnership": "108 runs (115 balls)",
                "source": f"Live Simulator ({reason})" if reason else "Live Simulator"
            },
            {
                "match_id": 90102,
                "series_name": "England Tour of West Indies 2024",
                "match_desc": "3rd ODI",
                "format": "ODI",
                "status": "Innings Break - England need 264 to win",
                "venue": "Kensington Oval",
                "city": "Bridgetown",
                "team1": "West Indies",
                "team1_short": "WI",
                "team1_runs": 263,
                "team1_wickets": 8,
                "team1_overs": 50.0,
                "team2": "England",
                "team2_short": "ENG",
                "team2_runs": 0,
                "team2_wickets": 0,
                "team2_overs": 0.0,
                "current_batters": [
                    {"name": "Jos Buttler", "runs": 0, "balls": 0, "fours": 0, "sixes": 0, "sr": 0.0},
                    {"name": "Phil Salt", "runs": 0, "balls": 0, "fours": 0, "sixes": 0, "sr": 0.0}
                ],
                "current_bowler": {"name": "Alzarri Joseph", "overs": 0.0, "maidens": 0, "runs": 0, "wickets": 0, "economy": 0.0},
                "partnership": "0 runs",
                "source": f"Live Simulator ({reason})" if reason else "Live Simulator"
            },
            {
                "match_id": 90103,
                "series_name": "ICC Men's T20 World Cup 2024",
                "match_desc": "Super 8 - Match 12",
                "format": "T20I",
                "status": "India won by 24 runs",
                "venue": "Daren Sammy National Cricket Stadium",
                "city": "Gros Islet",
                "team1": "India",
                "team1_short": "IND",
                "team1_runs": 205,
                "team1_wickets": 5,
                "team1_overs": 20.0,
                "team2": "Australia",
                "team2_short": "AUS",
                "team2_runs": 181,
                "team2_wickets": 7,
                "team2_overs": 20.0,
                "current_batters": [
                    {"name": "Rohit Sharma", "runs": 92, "balls": 41, "fours": 7, "sixes": 8, "sr": 224.39}
                ],
                "current_bowler": {"name": "Mitchell Starc", "overs": 4.0, "maidens": 0, "runs": 45, "wickets": 2, "economy": 11.25},
                "partnership": "Match Completed",
                "source": f"Live Simulator ({reason})" if reason else "Live Simulator"
            }
        ]
