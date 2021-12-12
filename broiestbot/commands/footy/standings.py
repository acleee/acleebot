"""Get team standings per league."""
from datetime import datetime
from typing import Optional

import requests
from emoji import emojize
from requests.exceptions import HTTPError

from config import (
    BUND_LEAGUE_ID,
    EPL_LEAGUE_ID,
    FOOTY_HTTP_HEADERS,
    FOOTY_STANDINGS_ENDPOINT,
    LIGA_LEAGUE_ID,
)
from logger import LOGGER


def epl_standings(endpoint: str) -> Optional[str]:
    """
    Get team standings table for EPL.

    :param str endpoint: Premiere league standings API endpoint.

    :returns: Optional[str]
    """
    try:
        standings_table = "\n\n\n\n"
        season = datetime.now().year
        params = {"league": EPL_LEAGUE_ID, "season": season}
        req = requests.get(FOOTY_STANDINGS_ENDPOINT, headers=FOOTY_HTTP_HEADERS, params=params)
        res = req.json()
        standings = res["response"][0]["league"]["standings"][0]
        for standing in standings:
            rank = standing["rank"]
            team = standing["team"]["name"]
            points = standing["points"]
            wins = standing["all"]["win"]
            draws = standing["all"]["draw"]
            losses = standing["all"]["lose"]
            standings_table = standings_table + f"{rank}. {team}: {points}pts ({wins}-{draws}-{losses})\n"
        if standings_table != "\n\n\n\n":
            return standings_table
        return emojize(":warning: Couldn't fetch standings :( :warning:", use_aliases=True)
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching EPL standings: {e.response.content}")
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching EPL standings: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching EPL standings: {e}")


def liga_standings(endpoint: str) -> Optional[str]:
    """
    Get standings table for La Liga.

    :param str endpoint: La Liga standings API endpoint.

    :returns: Optional[str]
    """
    try:
        standings_table = "\n\n\n\n"
        season = datetime.now().year
        params = {"league": LIGA_LEAGUE_ID, "season": season}
        req = requests.get(FOOTY_STANDINGS_ENDPOINT, headers=FOOTY_HTTP_HEADERS, params=params)
        res = req.json()
        standings = res["response"][0]["league"]["standings"][0]
        for standing in standings:
            rank = standing["rank"]
            team = standing["team"]["name"]
            points = standing["points"]
            wins = standing["all"]["win"]
            draws = standing["all"]["draw"]
            losses = standing["all"]["lose"]
            standings_table = standings_table + f"{rank}. {team}: {points}pts ({wins}-{draws}-{losses})\n"
        if standings_table != "\n\n\n\n":
            return standings_table
        return emojize(":warning: Couldn't fetch standings :( :warning:", use_aliases=True)
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching LIGA standings: {e.response.content}")
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching LIGA standings: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching LIGA standings: {e}")


def bund_standings(endpoint: str) -> Optional[str]:
    """
    Get standings table for Bundesliga.

    :param str endpoint: Bundesliga standings API endpoint.

    :returns: Optional[str]
    """
    try:
        standings_table = "\n\n]\n"
        season = datetime.now().year
        params = {"league": BUND_LEAGUE_ID, "season": season}
        req = requests.get(FOOTY_STANDINGS_ENDPOINT, headers=FOOTY_HTTP_HEADERS, params=params)
        res = req.json()
        standings = res["response"][0]["league"]["standings"][0]
        for standing in standings:
            rank = standing["rank"]
            team = standing["team"]["name"]
            points = standing["points"]
            wins = standing["all"]["win"]
            draws = standing["all"]["draw"]
            losses = standing["all"]["lose"]
            standings_table = standings_table + f"{rank}. {team}: {points}pts ({wins}-{draws}-{losses})\n"
        if standings_table != "\n\n\n\n":
            return standings_table
        return emojize(":warning: Couldn't fetch standings :( :warning:", use_aliases=True)
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching BUND standings: {e.response.content}")
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching BUND standings: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching BUND standings: {e}")
