"""Fetch all (live & upcoming) NBA games for today."""
from datetime import datetime

import requests
from requests import Response
from requests.exceptions import HTTPError

from config import NBA_BASE_URL, NBA_SEASON_YEAR, RAPID_API_KEY
from logger import LOGGER


def today_nba_games() -> Response:
    """
    Fetch all NBA games for the current date.

    :returns: Response
    """
    try:
        endpoint = f"{NBA_BASE_URL}/games"
        params = {
            "timezone": "America/New_York",
            "season": NBA_SEASON_YEAR,
            "league": "12",
            "date": datetime.now().strftime("%Y-%m-%d"),
        }
        headers = {
            "X-RapidAPI-Host": "api-basketball.p.rapidapi.com",
            "X-RapidAPI-Key": RAPID_API_KEY,
        }
        return requests.get(endpoint, headers=headers, params=params)
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching today's NBA games: {e.response.content}")
    except LookupError as e:
        LOGGER.error(f"LookupError while fetching today's NBA games: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching today's NBA games: {e}")
