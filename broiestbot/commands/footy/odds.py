from typing import List, Optional

import requests
from emoji import emojize
from requests.exceptions import HTTPError

from config import RAPID_API_KEY, HTTP_REQUEST_TIMEOUT
from logger import LOGGER


def get_footy_odds():
    try:
        url = "https://odds.p.rapidapi.com/v1/odds"
        querystring = {
            "sport": "soccer_epl",
            "region": "uk",
            "mkt": "h2h",
            "dateFormat": "iso",
            "oddsFormat": "decimal",
        }
        headers = {
            "x-rapidapi-host": "odds.p.rapidapi.com",
            "x-rapidapi-key": RAPID_API_KEY,
        }
        response = []
        resp = requests.get(url, headers=headers, params=querystring, timeout=HTTP_REQUEST_TIMEOUT)
        fixtures = resp.json().get("data")[::5]
        if resp.json().get("success"):
            response += get_fixture_odds(fixtures)
        return "\n\n".join(response)
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching footy odds: {e.response.content}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching footy odds: {e}")
        return emojize(f":yellow_square: idk what happened bot died rip :yellow_square:", language="en")


def get_fixture_odds(fixtures: List[dict]) -> Optional[str]:
    """
    :param List[dict] fixtures: Next 5 EPL fixtures
    """
    fixture_odds = ""
    for i, fixture in enumerate(fixtures):
        teams = fixture["teams"]
        home_team = f"{teams[0]} (home)"
        away_team = teams[1]
        odds = fixture["sites"][1]["odds"]["h2h"]
        fixture_odds += f"{home_team}: {odds[0]}\n \
                                        Draw: {odds[1]}\n \
                                        {away_team}: {odds[2]}"
        if fixture_odds:
            return emojize(f"\n\n\n\n:soccer: :moneybag: EPL ODDS\n\n{fixture_odds}", language="en")
    return None
