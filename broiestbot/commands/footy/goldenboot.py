"""Top scorers for a given league."""
from datetime import datetime

import requests
from emoji import emojize
from requests.exceptions import HTTPError

from config import EPL_LEAGUE_ID, FOOTY_HTTP_HEADERS, FOOTY_TOPSCORERS_ENDPOINT
from logger import LOGGER


def epl_golden_boot() -> str:
    """
    Fetch list of EPL golden boot top scorers.

    :return: str
    """
    golden_boot_leaders = "\n\n\n"
    try:
        season = datetime.now().year
        params = {"season": season, "league": EPL_LEAGUE_ID}
        req = requests.get(
            FOOTY_TOPSCORERS_ENDPOINT,
            headers=FOOTY_HTTP_HEADERS,
            params=params,
        )
        players = req.json().get("response")
        if players:
            for i, player in enumerate(players):
                name = player["player"]["name"]
                team = player["statistics"][0]["team"]["name"]
                goals = player["statistics"][0]["goals"]["total"]
                assists = player["statistics"][0]["goals"].get("assists", 0)
                shots_on = player["statistics"][0]["shots"].get("on", 0)
                shots_total = player["statistics"][0]["shots"].get("total", 0)
                if assists is None:
                    assists = 0
                golden_boot_leaders += f"{goals} - {name}, {team}  ({assists} assists, {shots_on}/{shots_total} SOG)\n"
                if i > 9:
                    break
            return golden_boot_leaders
        return emojize(
            f":warning: Couldn't find golden boot leaders; has season started yet? :warning:",
            use_aliases=True,
        )
    except HTTPError as e:
        LOGGER.error(
            f"HTTPError while fetching golden boot leaders: {e.response.content}"
        )
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching golden boot leaders: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching golden boot leaders: {e}")
