"""Fetch NBA standings."""
import requests
from requests.exceptions import HTTPError

from config import NBA_API_KEY, NBA_CONFERENCE_NAMES
from logger import LOGGER


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
        LOGGER.error(f"HTTPError while fetching NBA standings: {e.response.content}")
    except LookupError as e:
        LOGGER.error(f"LookupError while fetching NBA standings: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching NBA standings: {e}")
