"""Fetch or parse scheduled Phillies games."""
from datetime import datetime
from typing import Optional, Tuple

import requests
from emoji import emojize
from requests.exceptions import HTTPError

from config import MLB_BASE_ENDPOINT, RAPID_API_KEY, TIMEZONE_US_EASTERN, HTTP_REQUEST_TIMEOUT
from logger import LOGGER


def parse_upcoming_mlb_game(game: dict) -> Optional[str]:
    """
    Fetch upcoming MLB match-up scheduled for the current date.

    :param dict game: Dictionary response of an upcoming game summary.

    :returns: Optional[str]
    """
    try:
        home_name = game["teams"]["home"]["name"]
        away_name = game["teams"]["away"]["name"]
        away_stats, home_stats = get_team_stats(game)
        now = datetime.now(tz=TIMEZONE_US_EASTERN)
        start_time_hour = int(game["time"].split(":")[0])
        start_time_minute = int(game["time"].split(":")[0])
        start_datetime = now.replace(hour=start_time_hour, minute=start_time_minute, second=0)
        start_time = start_datetime.strftime("%I:%M%p").lower()
        return emojize(
            f":baseball: <b>{away_name}</b> @ <b>{home_name}</b> \n"
            f":input_numbers: {away_stats} - {home_stats}\n"
            f":nine_o’clock: Today, {start_time}",
            language="en",
        )
    except ValueError as e:
        LOGGER.error(f"ValueError while parsing upcoming Phillies game: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error while parsing upcoming Phillies game: {e}")


def get_team_stats(game: dict) -> Tuple[str, str]:
    try:
        away_id = str(game["teams"]["away"]["id"])
        home_id = str(game["teams"]["home"]["id"])
        away_stats = fetch_team_statistics(away_id)
        home_stats = fetch_team_statistics(home_id)
        away_wins = away_stats["games"]["wins"]["all"]["total"]
        away_losses = away_stats["games"]["loses"]["all"]["total"]
        away_win_pct = away_stats["games"]["wins"]["all"]["percentage"]
        home_wins = home_stats["games"]["wins"]["all"]["total"]
        home_losses = home_stats["games"]["loses"]["all"]["total"]
        home_win_pct = home_stats["games"]["wins"]["all"]["percentage"]
        return (
            f"{away_wins}W-{away_losses}L ({away_win_pct})",
            f"{home_wins}W-{home_losses}L ({home_win_pct})",
        )
    except ValueError as e:
        LOGGER.error(f"ValueError while parsing MLB team stats: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error while parsing MLB team stats: {e}")


def fetch_team_statistics(team_id: str) -> Optional[dict]:
    """
    Fetch high-level team stats for upcoming match-up.

    :param str team_id: Unique ID of team to fetch.

    :returns: Optional[dict]
    """
    try:
        url = f"{MLB_BASE_ENDPOINT}/teams/statistics"
        querystring = {"league": "1", "season": str(datetime.now().year), "team": team_id}
        headers = {
            "X-RapidAPI-Host": "api-baseball.p.rapidapi.com",
            "X-RapidAPI-Key": RAPID_API_KEY,
        }
        resp = requests.get(url, headers=headers, params=querystring, timeout=HTTP_REQUEST_TIMEOUT)
        if resp.status_code == 200 and resp.json():
            return resp.json().get("response")
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching MLB team stats: {e.response.content}")
    except ValueError as e:
        LOGGER.error(f"ValueError while fetching MLB team stats: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching MLB team stats: {e}")
