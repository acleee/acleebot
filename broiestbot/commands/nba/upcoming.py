"""Fetch upcoming NBA games for today."""
from datetime import datetime

import requests
from emoji import emojize
from requests.exceptions import HTTPError

from config import RAPID_API_KEY
from logger import LOGGER


def today_upcoming_nba_games():
    """Fetch upcoming NBA games"""
    try:
        games = "\n\n\n"
        endpoint = "https://api-basketball.p.rapidapi.com/games"
        params = {
            "timezone": "America/New_York",
            "season": "2021-2022",
            "league": "12",
            "date": datetime.now().strftime("%Y-%m-%d"),
        }
        headers = {
            "X-RapidAPI-Host": "api-basketball.p.rapidapi.com",
            "X-RapidAPI-Key": RAPID_API_KEY,
        }
        resp = requests.get(endpoint, headers=headers, params=params)
        if resp.status_code == 200 and len(resp.json()["response"]) > 0:
            games += emojize(":basketball: <b>NBA Games Today:</b>\n", use_aliases=True)
            for game in resp.json()["response"]:
                if game["status"]["short"] != "FT":
                    away_team = game["teams"]["away"]["name"]
                    home_team = game["teams"]["home"]["name"]
                    game_start_raw = datetime.strptime(game["time"], "%H:%M")
                    game_start = f"({game_start_raw.hour - 12}:{game_start_raw.minute:02d}pm)"
                    games += f"{away_team} @ {home_team} {game_start}\n"
            return games
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching NBA games: {e.response.content}")
    except LookupError as e:
        LOGGER.error(f"LookupError while fetching NBA games: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching NBA games: {e}")
