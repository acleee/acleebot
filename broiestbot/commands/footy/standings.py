"""Get team standings per league."""
import json
from typing import Optional

import requests
from emoji import emojize
from requests.exceptions import HTTPError

from config import RAPID_HTTP_HEADERS
from logger import LOGGER


def epl_standings(endpoint: str) -> Optional[str]:
    """
    Get team standings table for EPL.

    :param str endpoint: Premiere league standings API endpoint.

    :returns: Optional[str]
    """
    try:
        standings_table = "\n\n"
        req = requests.get(endpoint, headers=RAPID_HTTP_HEADERS)
        req = json.loads(req.text)
        standings = req["api"]["standings"][0]
        for standing in standings:
            rank = standing["rank"]
            team = standing["teamName"]
            points = standing["points"]
            wins = standing["all"]["win"]
            draws = standing["all"]["draw"]
            losses = standing["all"]["lose"]
            standings_table = (
                standings_table
                + f"{rank}. {team}: {points}pts ({wins}-{draws}-{losses})\n"
            )
        if standings_table != "\n\n":
            return standings_table
        return emojize(
            ":warning: Couldn't fetch standings :( :warning:", use_aliases=True
        )
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
        standings_table = "\n\n"
        req = requests.get(endpoint, headers=RAPID_HTTP_HEADERS)
        req = json.loads(req.text)
        standings = req["api"]["standings"][0]
        for standing in standings:
            rank = standing["rank"]
            team = standing["teamName"]
            points = standing["points"]
            wins = standing["all"]["win"]
            draws = standing["all"]["draw"]
            losses = standing["all"]["lose"]
            standings_table = (
                standings_table
                + f"{rank}. {team}: {points}pts ({wins}-{draws}-{losses})\n"
            )
        if standings_table != "\n\n":
            return standings_table
        return emojize(
            ":warning: Couldn't fetch standings :( :warning:", use_aliases=True
        )
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
        standings_table = "\n\n"
        req = requests.get(endpoint, headers=RAPID_HTTP_HEADERS)
        req = json.loads(req.text)
        standings = req["api"]["standings"][0]
        for standing in standings:
            rank = standing["rank"]
            team = standing["teamName"]
            points = standing["points"]
            wins = standing["all"]["win"]
            draws = standing["all"]["draw"]
            losses = standing["all"]["lose"]
            standings_table = (
                standings_table
                + f"{rank}. {team}: {points}pts ({wins}-{draws}-{losses})\n"
            )
        if standings_table != "\n\n":
            return standings_table
        return emojize(
            ":warning: Couldn't fetch standings :( :warning:", use_aliases=True
        )
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching BUND standings: {e.response.content}")
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching BUND standings: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching BUND standings: {e}")
