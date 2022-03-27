"""Fetch upcoming NBA games for today."""
from datetime import datetime

import requests
from emoji import emojize
from requests import Response
from requests.exceptions import HTTPError

from config import NBA_BASE_URL, RAPID_API_KEY
from logger import LOGGER


def today_upcoming_nba_games() -> str:
    """
    Fetch all NBA games for the current date.

    :returns: str
    """
    try:
        games = "\n\n\n"
        resp = today_nba_games()
        if resp.status_code == 200:
            upcoming_games = [
                game for game in resp.json()["response"] if game["status"]["short"] == "NS"
            ]
            if len(upcoming_games) > 0:
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


def live_nba_games() -> str:
    """
    Fetch all live NBA games.

    :returns: str
    """
    try:
        games = "\n\n\n"
        resp = today_nba_games()
        if resp.status_code == 200:
            live_games = [
                game
                for game in resp.json()["response"]
                if game["status"]["short"] != "NS" and game["status"]["short"] != "FT"
            ]
            if len(live_games) > 0:
                games += emojize(":basketball: <b>Live NBA Games:</b>\n", use_aliases=True)
                for game in live_games:
                    away_team = game["teams"]["away"]["name"]
                    away_team_score = game["scores"]["away"]["total"]
                    home_team = game["teams"]["home"]["name"]
                    home_team_score = game["scores"]["home"]["total"]
                    game_clock = game["status"]["timer"]
                    games += f"{away_team} <b>{away_team_score}</b> @ {home_team} <b>{home_team_score}</b>\n{game_clock}"
                return games
            elif len(resp.json()["response"]) > 0:
                upcoming_games = today_upcoming_nba_games()
                games += f"No live NBA games. Upcoming games today:\n"
                games += upcoming_games
                return games
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching NBA games: {e.response.content}")
    except LookupError as e:
        LOGGER.error(f"LookupError while fetching NBA games: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching NBA games: {e}")


def today_nba_games() -> Response:
    """
    Fetch all NBA games for the current date.

    :returns: Response
    """
    try:
        endpoint = f"{NBA_BASE_URL}/games"
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
        return requests.get(endpoint, headers=headers, params=params)
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching NBA games: {e.response.content}")
    except LookupError as e:
        LOGGER.error(f"LookupError while fetching NBA games: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching NBA games: {e}")
