"""Get team standings per league."""
from typing import Optional

import requests
from emoji import emojize
from requests.exceptions import HTTPError

from config import (
    FOOTY_HTTP_HEADERS,
    FOOTY_STANDINGS_ENDPOINT,
    HTTP_REQUEST_TIMEOUT,
)
from logger import LOGGER

from .util import get_season_year


def league_table_standings(LEAGUE_ID: int) -> Optional[str]:
    """
    Get table standings for a given league.

    :param int LEAGUE_ID: ID of league to get table standings for.

    :returns: Optional[str]
    """
    try:
        standings_table = "\n\n\n\n"
        params = {"league": LEAGUE_ID, "season": get_season_year(LEAGUE_ID)}
        req = requests.get(
            FOOTY_STANDINGS_ENDPOINT,
            headers=FOOTY_HTTP_HEADERS,
            params=params,
            timeout=HTTP_REQUEST_TIMEOUT,
        )
        res = req.json()
        standings = res["response"][0]["league"]["standings"][0]
        for standing in standings:
            rank = standing["rank"]
            team = standing["team"]["name"]
            points = standing["points"]
            wins = standing["all"]["win"]
            draws = standing["all"]["draw"]
            losses = standing["all"]["lose"]
            standings_table = standings_table + f"{rank}. {team}: {points}pts ({wins}w-{draws}d-{losses}l)\n"
        if standings_table != "\n\n\n\n":
            return standings_table
        return emojize(":warning: Couldn't fetch standings :warning:", language="en")
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching {LEAGUE_ID} standings: {e.response.content}")
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching {LEAGUE_ID} standings: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching {LEAGUE_ID} standings: {e}")
