"""Get team standings for a given league."""
from typing import Optional

import requests
from emoji import emojize
from requests.exceptions import HTTPError

from config import (
    FOOTY_HTTP_HEADERS,
    FOOTY_STANDINGS_ENDPOINT,
    HTTP_REQUEST_TIMEOUT,
    MLS_LEAGUE_ID,
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
                    standings_table + f"<b>{rank:5}. {team}</b>: {points}pts <i>({wins}W {draws}D {losses}L)</i>\n"
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


def mls_standings() -> Optional[str]:
    """
    Fetch and parse standings for MLS (regular season).

    :returns: Optional[str]
    """
    try:
        mls_standings_response = fetch_league_table_standings(MLS_LEAGUE_ID)
        if mls_standings_response:
            standings_table = "\n\n\n\n"
            for i, conference in enumerate(mls_standings_response[0]["league"]["standings"]):
                standings_table += mls_conference_standings(conference)
                if i == 0:
                    standings_table += "\n\n"
                elif standings_table != "\n\n\n\n":
                    return emojize(standings_table, language="en")
        return emojize(":warning: Couldn't fetch standings :warning:", language="en")
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching {MLS_LEAGUE_ID} standings: {e.response.content}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching {MLS_LEAGUE_ID} standings: {e}")


def mls_conference_standings(conference_standings: dict):
    """
    Parse standings for a given MLS conference.

    :param dict conference_standings: MLS standings for East OR West conference.

    :returns: str
    """
    try:
        conference_standings_table = ""
        conference_standings_table += f"<b>{conference_standings[0]['group']}</b>\n"
        for standing in conference_standings:
            rank = standing["rank"]
            team = standing["team"]["name"]
            points = standing["points"]
            wins = standing["all"]["win"]
            draws = standing["all"]["draw"]
            losses = standing["all"]["lose"]
            goalDiff = standing["goalsDiff"]
            form = (
                standing["form"]
                .replace("W", ":green_circle:")
                .replace("L", ":red_circle:")
                .replace("D", ":white_circle:")
            )
            conference_standings_table += f"{points} {team} <i>({wins}W {draws}D {losses}L, {goalDiff}GD)</i> {form}\n"
        if conference_standings_table != "":
            return f"{conference_standings_table}\n"
    except KeyError as e:
        LOGGER.error(f"KeyError when parsing MLS conference standings: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when parsing MLS conference standings: {e}")
