"""Fetch lineups before kickoff or during the match."""
from datetime import date
from typing import Optional

import requests
from emoji import emojize
from requests.exceptions import HTTPError

from config import (
    FOOTY_FIXTURES_ENDPOINT,
    FOOTY_HTTP_HEADERS,
    FOOTY_TEAMS_PRIORITY,
    FOOTY_XI_ENDPOINT,
)
from logger import LOGGER

from .util import get_preferred_timezone


def footy_team_lineups(room: str, username: str) -> str:
    """
    Fetch starting lineups by team for immediate or live fixtures.

    :param str room: Chatango room in which command was triggered.
    :param str username: Name of user who triggered the command.

    :returns: str
    """
    team_fixtures = "\n\n\n\n"
    for team_name, team_id in FOOTY_TEAMS_PRIORITY.items():
        team_fixture = fetch_fixture_by_team(team_id, room, username)
        if bool(team_fixture):
            team_fixtures.append(team_fixture)
        else:
            team_fixture = fetch_fixture_by_team(team_id, room, username)
            team_fixtures += team_fixtures + "\n"
    if team_fixtures != "\n\n\n\n":
        pass  # TODO: Finish logic
    return emojize(
        ":warning: Couldn't find any upcoming fixtures :( :warning:", use_aliases=True
    )


def fetch_fixture_by_team(team_id: int, room: str, username: str) -> Optional[dict]:
    """
    Get team's fixture scheduled for today.

    :param int team_id: ID of team.
    :param str room: Chatango room in which command was triggered.
    :param str username: Name of user who triggered the command.

    :returns: Optional[dict]
    """
    try:
        today = date.strftime("%y-%m-%d")
        params = {"team": team_id, "date": today, "next": 1}
        params.update(get_preferred_timezone(room, username))
        req = requests.get(
            FOOTY_FIXTURES_ENDPOINT,
            headers=FOOTY_HTTP_HEADERS,
            params=params,
        )
        return req.json().get("response")
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching footy fixtures: {e.response.content}")
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching footy fixtures: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching footy fixtures: {e}")


def get_xi_per_fixture_team(fixture_id: str) -> str:
    """
    Get team lineup for given fixture.

    :param str fixture_id: ID of an upcoming fixture.

    :returns: str
    """
    lineups = "\n\n\n\n"
    params = {"fixture": fixture_id}
    resp = requests.get(FOOTY_XI_ENDPOINT, headers=FOOTY_HTTP_HEADERS, params=params)
    team_lineups = resp.json().get("response")
    if bool(team_lineups) is not False:
        for lineup in team_lineups:
            lineups += format_team_lineup(lineup)
    if lineups != "\n\n\n\n":
        return lineups
    return emojize(
        f":soccer_ball: :cross_mark: sry no fixtures today :( :cross_mark: :soccer_ball:",
        use_aliases=True,
    )


def format_team_lineup(lineup):
    formation = lineup.get("formation")
    for player in lineup["startXI"]:
        pass
