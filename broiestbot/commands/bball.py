"""Fetch live basketball scores."""
import requests
from emoji import emojize
from requests.exceptions import HTTPError

from config import NBA_API_KEY, NBA_CONFERENCE_NAMES, RAPID_API_KEY
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
    except LookupError as e:
        LOGGER.error(f"LookupError while fetching squeekfloor games: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching squeekfloor games: {e}")


def nba_standings() -> str:
    """Fetch NBA team standings for regular season."""
    try:
        standings = "\n\n\n"
        for conference in NBA_CONFERENCE_NAMES:
            params = {
                "league": "12",
                "season": "2021-2022",
                "group": conference,
                "stage": "NBA - Regular Season",
            }
            endpoint = "https://api-basketball.p.rapidapi.com/standings"
            headers = {
                "x-rapidapi-host": "api-basketball.p.rapidapi.com",
                "x-rapidapi-key": NBA_API_KEY,
            }
            resp = requests.request("GET", endpoint, headers=headers, params=params)
            if resp.status_code == 200:
                standings += f"{conference.upper()}\n"
                for team_info in resp.json()["response"][0]:
                    team_standing = f"{team_info['position']}. {team_info['team']['name']} {team_info['games']['win']['total']}-{team_info['games']['lose']['total']} ({team_info['games']['win']['percentage']})\n"
                    standings += team_standing
                standings += "\n"
        return standings
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching squeekfloor standings: {e.response.content}")
    except LookupError as e:
        LOGGER.error(f"LookupError while fetching squeekfloor standings: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching squeekfloor standings: {e}")
