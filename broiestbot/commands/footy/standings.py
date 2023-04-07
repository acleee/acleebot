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


def league_table_standings(league_id: int) -> Optional[str]:
    """
    Get table standings for a given league.

    :param int league_id: ID of league to get table standings for.

    :returns: Optional[str]
    """
    try:
        league_table_response = fetch_league_table_standings(league_id)
        if league_table_response:
            standings_table = "\n\n\n\n"
            standings = league_table_response[0]["league"]["standings"][0]
            for standing in standings:
                rank = standing["rank"]
                team = standing["team"]["name"]
                points = standing["points"]
                wins = standing["all"]["win"]
                draws = standing["all"]["draw"]
                losses = standing["all"]["lose"]
                standings_table = (
                    standings_table + f"<b>{rank:3}. {team:20}</b>: <i>{points}pts</i> ({wins}W {draws}D {losses}L)\n"
                )
            if standings_table != "\n\n\n\n":
                return standings_table
        return emojize(":warning: Couldn't fetch standings :warning:", language="en")
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching {league_id} standings: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching {league_id} standings: {e}")


def fetch_league_table_standings(league_id: int) -> Optional[dict]:
    """
    Fetch league table standings for a given league.

    :param int league_id: ID of league to get table standings for.

    :returns: Optional[dict]
    """
    try:
        params = {"league": league_id, "season": get_season_year(league_id)}
        resp = requests.get(
            FOOTY_STANDINGS_ENDPOINT,
            headers=FOOTY_HTTP_HEADERS,
            params=params,
            timeout=HTTP_REQUEST_TIMEOUT,
        )
        if resp.status_code == 200:
            return resp.json().get("response")
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching {league_id} standings: {e.response.content}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching {league_id} standings: {e}")
