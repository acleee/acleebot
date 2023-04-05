"""Parse schedule of today's upcoming NBA games."""
from datetime import datetime

from emoji import emojize

from logger import LOGGER

from .today import today_nba_games


def upcoming_nba_games() -> str:
    """
    Fetch all NBA games for the current date.

    :returns: str
    """
    try:
        games = "\n\n\n"
        resp = today_nba_games()
        if resp.status_code == 200:
            upcoming_games = [game for game in resp.json()["response"] if game["status"]["short"] == "NS"]
            if len(upcoming_games) > 0:
                games += emojize(":basketball: <b>NBA Games Today:</b>\n", language="en")
                for game in resp.json().get("response"):
                    if game["status"]["short"] != "FT":
                        away_team = game["teams"]["away"]["name"]
                        home_team = game["teams"]["home"]["name"]
                        game_start_raw = datetime.strptime(game["time"], "%H:%M")
                        game_start = f"({game_start_raw.hour - 12}:{game_start_raw.minute:02d}pm)"
                        games += f"{away_team} @ {home_team} {game_start}\n"
                return games
    except LookupError as e:
        LOGGER.error(f"LookupError while fetching NBA games: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching NBA games: {e}")
