"""Fetch scheduled fixtures across leagues for today only."""
from datetime import datetime, timedelta
from typing import Optional

import requests
from emoji import emojize
from requests.exceptions import HTTPError

from config import (
    CHATANGO_OBI_ROOM,
    FOOTY_FIXTURES_ENDPOINT,
    FOOTY_HTTP_HEADERS,
    FOOTY_LEAGUES,
)
from logger import LOGGER

from .util import get_preferred_time_format, get_preferred_timezone


def footy_todays_upcoming_fixtures(room: str, username: str) -> str:
    """
    Fetch upcoming fixtures within 1 week for EPL, LIGA, BUND, FA, UCL, EUROPA, etc.

    :param str room: Chatango room in which command was triggered.
    :param str username: Name of user who triggered the command.

    :returns: str
    """
    upcoming_fixtures = "\n\n\n\n"
    for league_name, league_id in FOOTY_LEAGUES.items():
        league_fixtures = footy_todays_upcoming_fixtures_per_league(
            league_name, league_id, room, username
        )
        if league_fixtures is not None:
            upcoming_fixtures += league_fixtures + "\n"
    if upcoming_fixtures != "\n\n":
        return upcoming_fixtures
    return emojize(
        ":warning: Couldn't find any upcoming fixtures :( :warning:", use_aliases=True
    )


def footy_todays_upcoming_fixtures_per_league(
    league_name: str, league_id: int, room: str, username: str
) -> Optional[str]:
    """
    Get this week's upcoming fixtures for a given league or tournament.

    :param str league_name: Name of footy league/cup.
    :param int league_id: ID of footy league/cup.
    :param str room: Chatango room in which command was triggered.
    :param str username: Name of user who triggered the command.

    :returns: Optional[str]
    """
    try:
        league_upcoming_fixtures = ""
        fixtures = todays_upcoming_fixtures_by_league(league_id)
        if fixtures and len(fixtures) > 0:
            for i, fixture in enumerate(fixtures):
                date = datetime.strptime(
                    fixture["fixture"]["date"], "%Y-%m-%dT%H:%M:%S%z"
                )
                display_date, tz = get_preferred_time_format(date, room, username)
                if room == CHATANGO_OBI_ROOM:
                    display_date, tz = get_preferred_time_format(date, room, username)
                if date - datetime.now(tz=tz) < timedelta(days=7):
                    if i == 0 and len(fixture) > 1:
                        league_upcoming_fixtures += emojize(
                            f"{league_name}:\n", use_aliases=True
                        )
                    league_upcoming_fixtures += add_upcoming_fixture(
                        fixture, date, room, username
                    )
            return league_upcoming_fixtures
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching footy fixtures: {e.response.content}")
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching footy fixtures: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching footy fixtures: {e}")


def todays_upcoming_fixtures_by_league(league_id: int) -> Optional[dict]:
    """
    Fetch next 5 upcoming fixtures for a given league.

    :param int league_id: ID of footy league/cup.

    :returns: Optional[dict]
    """
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        params = {
            "date": today,
            "league": league_id,
            "status": "NS",
            "timezone": "Europe/London",
            "season": datetime.now().year,
        }
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


def add_upcoming_fixture(
    fixture: dict, date: datetime, room: str, username: str
) -> str:
    """
    Construct upcoming fixture match-up.

    :param dict fixture: Scheduled fixture data.
    :param datetime date: Fixture start time/date displayed in preferred timezone.
    :param str room: Chatango room in which command was triggered.
    :param str username: Name of user who triggered the command.

    :returns: str
    """
    home_team = abbreviate_team_name(fixture["teams"]["home"]["name"])
    away_team = abbreviate_team_name(fixture["teams"]["away"]["name"])
    display_date, tz = get_preferred_time_format(date, room, username)
    return f"{away_team} @ {home_team} - {display_date}\n"


def abbreviate_team_name(team_name: str) -> str:
    """
    Abbreviate long team names to make schedules readable.

    :param str team_name: Full team name.

    :returns: str
    """
    return (
        team_name.replace("New England", "NE")
        .replace("New York City", "NYC")
        .replace("New York", "NY")
        .replace("Paris Saint Germain", "PSG")
        .replace("Manchester United", "ManU")
        .replace("Manchester City", "Man City")
        .replace("Liverpool", "LFC")
        .replace("Philadelphia", "PHI")
    )
