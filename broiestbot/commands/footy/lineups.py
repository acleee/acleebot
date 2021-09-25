"""Fetch lineups before kickoff or during the match."""
from datetime import date, datetime, timedelta
from typing import Optional

import requests
from emoji import emojize
from logger import LOGGER
from requests.exceptions import HTTPError

from config import (
    CHATANGO_OBI_ROOM,
    FOOTY_FIXTURES_ENDPOINT,
    FOOTY_HTTP_HEADERS,
    FOOTY_LEAGUES,
    FOOTY_TEAMS_PRIORITY,
)

from .util import get_preferred_time_format, get_preferred_timezone


def footy_team_lineups(room: str, username: str) -> str:
    """
    Fetch starting lineups by team for immediate or live fixtures.

    :param str room: Chatango room in which command was triggered.
    :param str username: Name of user who triggered the command.

    :returns: str
    """
    team_fixtures = []
    season = datetime.now().year
    for team_name, team_id in FOOTY_TEAMS_PRIORITY.items():
        team_fixture = footy_upcoming_fixture_per_team(team_id, room, username, season)
        if bool(team_fixture):
            team_fixtures.append(team_fixture)
        else:
            season - 1
            team_fixture = footy_upcoming_fixture_per_team(
                team_id, room, username, season
            )
            team_fixtures += team_fixtures + "\n"
    if bool(team_fixture):
        pass  # TODO: Finish logic
    return emojize(
        ":warning: Couldn't find any upcoming fixtures :( :warning:", use_aliases=True
    )


def fetch_fixture_by_team(
    team_id: int, room: str, username: str, season: int
) -> Optional[dict]:
    """
    Get team's fixture acheduled for today.

    :param int team_id: ID of team.
    :param str room: Chatango room in which command was triggered.
    :param str username: Name of user who triggered the command.

    :returns: Optional[dict]
    """
    try:
        today = date.strftime("%y-%m-%d")
        params = {"team": team_id, "date": today, "season": season, "next": 1}
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


def get_xi_per_fixture_team(fixture_id: str, team_id: str):
    """
    Get team lineup for given fixture.

    """
    params = {"id": fixture_id}
    req = requests.get(
        FOOTY_FIXTURES_ENDPOINT, headers=FOOTY_HTTP_HEADERS, params=params
    )
