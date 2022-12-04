"""Fetch lineups before kickoff or during the match."""
from datetime import datetime
from typing import Optional

import requests
from emoji import emojize
from requests.exceptions import HTTPError

from config import (
    FOOTY_HTTP_HEADERS,
    FOOTY_LEAGUES_LINEUPS,
    FOOTY_XI_ENDPOINT,
    HTTP_REQUEST_TIMEOUT,
)
from logger import LOGGER

from .today import fetch_today_fixtures_by_league, parse_upcoming_fixture


def footy_upcoming_lineups(room: str, username: str) -> str:
    """
    Fetch starting lineups by team for immediate or live fixtures.

    :param str room: Chatango room in which command was triggered.
    :param str username: Name of user who triggered the command.

    :returns: str
    """
    today_fixture_lineups = "\n\n\n\n"
    for league_name, league_id in FOOTY_LEAGUES_LINEUPS.items():
        today_fixtures = fetch_today_fixtures_by_league(league_id, room, username)
        today_fixture_lineups += emojize(f"<b>{league_name}</b>\n", language="en")
        if bool(today_fixtures):
            for fixture in today_fixtures:
                fixture_start_time = datetime.strptime(
                    fixture["fixture"]["date"], "%Y-%m-%dT%H:%M:%S%z"
                )
                lineups = fetch_lineups_per_fixture(fixture["fixture"]["id"])
                today_fixture_lineups += parse_upcoming_fixture(
                    fixture, fixture_start_time, room, username
                )
                if lineups:
                    today_fixture_lineups += get_fixture_xis(lineups)
                else:
                    today_fixture_lineups += "<i>Lineups not available yet<i>\n\n"
            return today_fixture_lineups
    return f"@{username} No footy XIs available yet."


def fetch_lineups_per_fixture(fixture_id: str) -> Optional[dict]:
    """
    Get team lineup for given fixture.

    :param str fixture_id: ID of an upcoming fixture.

    :returns: dict
    """
    try:
        params = {"fixture": fixture_id}
        resp = requests.get(
            FOOTY_XI_ENDPOINT,
            headers=FOOTY_HTTP_HEADERS,
            params=params,
            timeout=HTTP_REQUEST_TIMEOUT,
        )
        team_lineups = resp.json().get("response")
        if resp.status_code == 200 and team_lineups:
            return team_lineups
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching footy XIs: {e.response.content}")
    except ValueError as e:
        LOGGER.error(f"ValueError while fetching footy XIs: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching footy XIs: {e}")


def get_fixture_xis(fixture_lineups: dict) -> str:
    """
    Parse & format player lineups for an upcoming fixture.

    :param dict fixture_lineups: JSON Response containing two lineups for a given fixture.

    :returns: str
    """
    try:
        lineups_response = ""
        for lineup in fixture_lineups:
            team = lineup["team"]["name"]
            formation = lineup["formation"]
            coach = lineup["coach"]["name"]
            players = "\n".join(
                [
                    f"<b>{player['pos']}</b> {player['name']} (#{player['number']})"
                    for player in lineup["startXI"]
                ]
            )
            lineups_response += f"<b>{team}<b> {formation}\n" f"{coach}\n" f"{players}\n\n"
        return lineups_response
    except KeyError as e:
        LOGGER.error(f"KeyError while parsing footy XIs: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when parsing footy XIs: {e}")
