"""Fetch live basketball scores."""
import requests
from emoji import emojize
from requests.exceptions import HTTPError

from config import RAPID_API_KEY
from logger import LOGGER


def live_nba_games() -> str:
    try:
        endpoint = "https://livescore6.p.rapidapi.com/matches/v2/list-by-date"
        params = {"Category": "basketball", "Date": "20210521"}
        headers = {
            "content-type": "application/json",
            "x-rapidapi-key": RAPID_API_KEY,
            "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
        }
        req = requests.get(endpoint, headers=headers, params=params)
        if req.status_code == 200:
            data = req.json()["Stages"][0]
            if data["Cid"] != "NBA":
                return emojize(
                    f":warning:️️ idk what happened I died :warning:",
                    use_aliases=True,
                )
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching squeekfloor games: {e.response.content}")
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching squeekfloor games: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching squeekfloor games: {e}")
