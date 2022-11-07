"""Get team standings per league."""
from typing import Optional

import requests
from emoji import emojize
from requests.exceptions import HTTPError

from config import (
    BUND_LEAGUE_ID,
    EFL_LEAGUE_ID,
    EPL_LEAGUE_ID,
    FOOTY_HTTP_HEADERS,
    FOOTY_STANDINGS_ENDPOINT,
    LIGA_LEAGUE_ID,
    LIGUE_ONE_ID, HTTP_REQUEST_TIMEOUT,
)
from logger import LOGGER

from .util import get_season_year


def epl_standings() -> Optional[str]:
    """
    Get EPL table standings.

    :returns: Optional[str]
    """
    try:
        standings_table = "\n\n\n\n"
        params = {"league": EPL_LEAGUE_ID, "season": get_season_year(EPL_LEAGUE_ID)}
        req = requests.get(FOOTY_STANDINGS_ENDPOINT, headers=FOOTY_HTTP_HEADERS, params=params, timeout=HTTP_REQUEST_TIMEOUT)
        res = req.json()
        standings = res["response"][0]["league"]["standings"][0]
        for standing in standings:
            rank = standing["rank"]
            team = standing["team"]["name"]
            points = standing["points"]
            wins = standing["all"]["win"]
            draws = standing["all"]["draw"]
            losses = standing["all"]["lose"]
            standings_table = (
                standings_table + f"{rank}. {team}: {points}pts ({wins}w-{draws}d-{losses}l)\n"
            )
        if standings_table != "\n\n\n\n":
            return standings_table
        return emojize(":warning: Couldn't fetch standings :( :warning:")
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching EPL standings: {e.response.content}")
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching EPL standings: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching EPL standings: {e}")


def liga_standings() -> Optional[str]:
    """
    Get Liga table standings.

    :returns: Optional[str]
    """
    try:
        standings_table = "\n\n\n\n"
        params = {"league": LIGA_LEAGUE_ID, "season": get_season_year(LIGA_LEAGUE_ID)}
        req = requests.get(FOOTY_STANDINGS_ENDPOINT, headers=FOOTY_HTTP_HEADERS, params=params, timeout=HTTP_REQUEST_TIMEOUT)
        res = req.json()
        standings = res["response"][0]["league"]["standings"][0]
        for standing in standings:
            rank = standing["rank"]
            team = standing["team"]["name"]
            points = standing["points"]
            wins = standing["all"]["win"]
            draws = standing["all"]["draw"]
            losses = standing["all"]["lose"]
            standings_table = (
                standings_table + f"{rank}. {team}: {points}pts ({wins}w-{draws}d-{losses}l)\n"
            )
        if standings_table != "\n\n\n\n":
            return standings_table
        return emojize(":warning: Couldn't fetch standings :( :warning:")
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching LIGA standings: {e.response.content}")
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching LIGA standings: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching LIGA standings: {e}")


def bund_standings() -> Optional[str]:
    """
    Get Bundesliga table standings.

    :returns: Optional[str]
    """
    try:
        standings_table = "\n\n]\n"
        params = {"league": BUND_LEAGUE_ID, "season": get_season_year(BUND_LEAGUE_ID)}
        req = requests.get(FOOTY_STANDINGS_ENDPOINT, headers=FOOTY_HTTP_HEADERS, params=params, timeout=HTTP_REQUEST_TIMEOUT)
        res = req.json()
        standings = res["response"][0]["league"]["standings"][0]
        for standing in standings:
            rank = standing["rank"]
            team = standing["team"]["name"]
            points = standing["points"]
            wins = standing["all"]["win"]
            draws = standing["all"]["draw"]
            losses = standing["all"]["lose"]
            standings_table = (
                standings_table + f"{rank}. {team}: {points}pts ({wins}w-{draws}d-{losses}l)\n"
            )
        if standings_table != "\n\n\n\n":
            return standings_table
        return emojize(":warning: Couldn't fetch standings :( :warning:")
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching BUND standings: {e.response.content}")
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching BUND standings: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching BUND standings: {e}")


def efl_standings() -> Optional[str]:
    """
    Get EFL table standings.

    :returns: Optional[str]
    """
    try:
        standings_table = "\n\n\n\n"
        params = {"league": EFL_LEAGUE_ID, "season": get_season_year(EFL_LEAGUE_ID)}
        req = requests.get(FOOTY_STANDINGS_ENDPOINT, headers=FOOTY_HTTP_HEADERS, params=params, timeout=HTTP_REQUEST_TIMEOUT)
        res = req.json()
        standings = res["response"][0]["league"]["standings"][0]
        for standing in standings:
            rank = standing["rank"]
            team = standing["team"]["name"]
            points = standing["points"]
            wins = standing["all"]["win"]
            draws = standing["all"]["draw"]
            losses = standing["all"]["lose"]
            standings_table = (
                standings_table + f"{rank}. {team}: {points}pts ({wins}w-{draws}d-{losses}l)\n"
            )
        if standings_table != "\n\n\n\n":
            return standings_table
        return emojize(":warning: Couldn't fetch standings :( :warning:")
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching EFL standings: {e.response.content}")
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching EFL standings: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching EFL standings: {e}")


def ligue_standings() -> Optional[str]:
    """
    Get Ligue 1 table standings.

    :returns: Optional[str]
    """
    try:
        standings_table = "\n\n\n\n"
        params = {"league": LIGUE_ONE_ID, "season": get_season_year(LIGUE_ONE_ID)}
        req = requests.get(FOOTY_STANDINGS_ENDPOINT, headers=FOOTY_HTTP_HEADERS, params=params, timeout=HTTP_REQUEST_TIMEOUT)
        res = req.json()
        standings = res["response"][0]["league"]["standings"][0]
        for standing in standings:
            rank = standing["rank"]
            team = standing["team"]["name"]
            points = standing["points"]
            wins = standing["all"]["win"]
            draws = standing["all"]["draw"]
            losses = standing["all"]["lose"]
            standings_table = (
                standings_table + f"{rank}. {team}: {points}pts ({wins}w-{draws}d-{losses}l)\n"
            )
        if standings_table != "\n\n\n\n":
            return standings_table
        return emojize(":warning: Couldn't fetch standings :( :warning:")
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching EFL standings: {e.response.content}")
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching EFL standings: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching EFL standings: {e}")
