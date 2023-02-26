"""Fetch lineups before kickoff or during the match."""
from datetime import datetime
from typing import List, Optional

import requests
from emoji import emojize
from requests.exceptions import HTTPError

from config import FOOTY_FIXTURES_ENDPOINT, FOOTY_HTTP_HEADERS, FOOTY_LEAGUES_LINEUPS, HTTP_REQUEST_TIMEOUT
from logger import LOGGER

from .util import (
    get_current_day,
    get_preferred_timezone,
    get_season_year,
)

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


def footy_team_lineups(room: str, username: str) -> str:
    """
    Fetch starting lineups by team for immediate or live fixtures.

    :param str room: Chatango room in which command was triggered.
    :param str username: Name of user who triggered the command.

    :returns: str
    """
    try:
        today_fixture_lineups = "\n\n\n\n"
        for league_name, league_id in FOOTY_LEAGUES_LINEUPS.items():
            league_fixtures = get_today_live_or_upcoming_fixtures(league_id, room, username)
            if league_fixtures is not None:
                today_fixture_lineups += emojize(f"<b>{league_name}</b>\n", language="en")
                for fixture in league_fixtures:
                    if fixture is not None:
                        fixture_id = fixture["fixture"]["id"]
                        lineups = fetch_lineups_per_fixture(fixture_id)
                        if lineups:
                            today_fixture_lineups += get_fixture_xis(lineups)
                            today_fixture_lineups += "\n\n----------------------\n\n"
                        else:
                            today_fixture_lineups += "<i>Lineups not available yet<i>\n\n"
        return today_fixture_lineups
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching footy XIs: {e}")


def fetch_lineups_per_fixture(fixture_id: int) -> Optional[dict]:
    """
    Get team lineup for given fixture.

    :param int fixture_id: ID of an upcoming fixture.

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
        return resp.json()["response"]
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching footy XIs: {e.response.content}")
    except ValueError as e:
        LOGGER.error(f"ValueError while fetching footy XIs: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching footy XIs: {e}")


def get_fixture_xis(teams: dict) -> str:
    """
    Parse & format player lineups for an upcoming fixture.

    :param dict teams: JSON Response containing two lineups for a given fixture.

    :returns: str
    """
    try:
        lineups_response = ""
        for team in teams:
            team_name = team["team"]["name"]
            formation = team["formation"]
            coach = team["coach"]["name"]
            players = "\n".join(
                [
                    f"<b>{player['player']['pos']}</b> {player['player']['name']} (#{player['player']['number']})"
                    for player in team["startXI"]
                ]
            )
            lineups_response += f"<b>{team_name}</b> {formation} ({coach})\n"
            lineups_response += f"{players}\n\n"
        return lineups_response
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching footy fixtures: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching footy fixtures: {e}")


def get_today_live_or_upcoming_fixtures(league_id: int, room: str, username: str) -> List[dict]:
    try:
        today = get_current_day(room)
        params = {
            "date": today.strftime("%Y-%m-%d"),
            "league": league_id,
            "season": get_season_year(league_id),
        }
        params.update(get_preferred_timezone(room, username))
        resp = requests.get(
            FOOTY_FIXTURES_ENDPOINT,
            headers=FOOTY_HTTP_HEADERS,
            params=params,
            timeout=HTTP_REQUEST_TIMEOUT,
        )
        return resp.json()["response"]
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching footy fixtures: {e.response.content}")
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching footy fixtures: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching footy fixtures: {e}")
