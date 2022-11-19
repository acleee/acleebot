"""Fetch Phillies MLB game summaries for the current date."""
from datetime import datetime
from typing import Optional

import pytz
import requests
from emoji import emojize
from requests.exceptions import HTTPError

from config import (
    MLB_BASE_ENDPOINT,
    MLB_LEAGUE_ID,
    MLB_PHILLIES_ID,
    RAPID_API_KEY,
    HTTP_REQUEST_TIMEOUT,
)
from logger import LOGGER

from .util import parse_mlb_game


def today_phillies_games() -> str:
    """
    Fetch live or upcoming Phillies games for the current date.

    :returns: str
    """
    today_games_response = "\n\n\n\n"
    today_games = get_today_games()
    if bool(today_games):
        for game in today_games:
            mlb_game = parse_mlb_game(game)
            if mlb_game is not None:
                today_games_response += parse_mlb_game(game)
                return today_games_response
    return emojize(":warning: Couldn't find any MLB games :( :warning:")


def get_today_games() -> Optional[dict]:
    """
    Fetch Phillies games scheduled for the current date.

    :returns: Optional[dict]
    """
    try:
        url = f"{MLB_BASE_ENDPOINT}/games"
        today = datetime.now(pytz.timezone("America/New_York")).strftime("%Y-%m-%d")
        params = {
            "league": MLB_LEAGUE_ID,
            "season": str(datetime.now().year),
            "team": MLB_PHILLIES_ID,
            "date": today,
            "timezone": "America/New_York",
        }
        headers = {
            "X-RapidAPI-Host": "api-baseball.p.rapidapi.com",
            "X-RapidAPI-Key": RAPID_API_KEY,
        }
        resp = requests.get(url, headers=headers, params=params, timeout=HTTP_REQUEST_TIMEOUT)
        if resp.status_code == 200 and resp.json():
            return resp.json().get("response")
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching MLB games: {e.response.content}")
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching MLB games: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching MLB games: {e}")
