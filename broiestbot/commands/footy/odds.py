from typing import List

import requests
from emoji import emojize
from logger import LOGGER
from requests.exceptions import HTTPError

from config import RAPID_API_KEY


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
        resp = requests.get(url, headers=headers, params=querystring)
        fixtures = resp.json().get("data")[::5]
        if resp.json().get("success"):
            fixture_odds = get_fixture_odds(fixtures)

        return emojize(
            f":yellow_square: idk what happened bot died rip :yellow_square:",
            use_aliases=True,
        )
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching footy odds: {e.response.content}")
    except IndexError as e:
        LOGGER.error(f"IndexError while fetching footy odds: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching footy odds: {e}")


def get_fixture_odds(fixtures: List[dict]):
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
                                        {away_team}: {odds[2]}\n\n"
        if fixture_odds:
            return emojize(
                f"\n\n\n\n:soccer: :moneybag: EPL ODDS\n\n{fixture_odds}",
                use_aliases=True,
            )
    return None

