import requests
from requests.exceptions import HTTPError

from config import RAPID_API_KEY
from logger import LOGGER


def get_footy_odds():
    try:
        fixture_odds = ""
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
        req = requests.get(url, headers=headers, params=querystring)
        res = req.json()
        if res["success"]:
            for fixture in req.json().get("data"):
                teams = fixture["teams"]
                home_team = fixture["home_team"]
                odds = fixture["sites"][1]["odds"]["h2h"]
                fixture_odds += f"{teams[0]}: {odds[0]}\n \
                               Draw: {odds[1]}\n \
                               {teams[1]}: {odds[2]}\n\n".replace(
                    home_team, f"{home_team} (home)"
                )
        return f"\n\n\nEPL ODDS\n\n{fixture_odds}"
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching footy odds: {e.response.content}")
    except IndexError as e:
        LOGGER.error(f"IndexError while fetching footy odds: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching footy odds: {e}")
