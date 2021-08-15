"""Fetch scheduled fixtures across leagues."""
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
    FOXES_TEAM_ID,
)
from logger import LOGGER

from .util import get_preferred_time_format, get_preferred_timezone


def footy_upcoming_fixtures(room: str, username: str) -> str:
    """
    Fetch upcoming fixtures within 1 week for EPL, LIGA, BUND, FA, UCL, EUROPA, etc.

    :param str room: Chatango room in which command was triggered.
    :param str username: Name of user who triggered the command.

    :returns: str
    """
    upcoming_fixtures = "\n\n"
    season = datetime.now().year
    for league_name, league_id in FOOTY_LEAGUES.items():
        league_fixtures = footy_upcoming_fixtures_per_league(
            league_name, league_id, room, username, season
        )
        if league_fixtures is not None:
            upcoming_fixtures += league_fixtures + "\n"
    if upcoming_fixtures != "\n\n":
        return upcoming_fixtures
    return emojize(
        ":warning: Couldn't find any upcoming fixtures :( :warning:", use_aliases=True
    )


def footy_upcoming_fixtures_per_league(
    league_name: str, league_id: int, room: str, username: str, season: int
) -> Optional[str]:
    """
    Get this week's upcoming fixtures for a given league or tournament.

    :param str league_name: Name of footy league/cup.
    :param int league_id: ID of footy league/cup.
    :param str room: Chatango room in which command was triggered.
    :param str username: Name of user who triggered the command.
    :param int season: Season year of league/cup.

    :returns: Optional[str]
    """
    try:
        upcoming_fixtures = ""
        fixtures = fetch_upcoming_fixtures(season, league_id, room, username)
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
                        upcoming_fixtures += emojize(
                            f"{league_name}:\n", use_aliases=True
                        )
                    upcoming_fixtures += add_upcoming_fixture(
                        fixture, date, room, username
                    )
            return upcoming_fixtures
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching footy fixtures: {e.response.content}")
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching footy fixtures: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching footy fixtures: {e}")


def fetch_upcoming_fixtures(
    season: int, league_id: int, room: str, username: str
) -> Optional[dict]:
    """
    Fetch next 5 upcoming fixtures for a given league.

    :param int season: Season year of league/cup.
    :param int league_id: ID of footy league/cup.
    :param str room: Chatango room in which command was triggered.
    :param str username: Name of user who triggered the command.

    :returns: Optional[dict]
    """
    try:
        params = {"season": season, "league": league_id, "next": 7, "status": "NS"}
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


def add_upcoming_fixture(
    fixture: dict, date: datetime, room: str, username: str
) -> str:
    """
    Construct upcoming fixture match-up.

    :param dict fixture: Scheduled fixture data.
    :param datetime date: Fixture start time/date defaulted to UTC time.
    :param str room: Chatango room in which command was triggered.
    :param str username: Name of user who triggered the command.

    :returns: str
    """
    home_team = fixture["teams"]["home"]["name"].replace(" U23", "").replace("W ", "")
    away_team = fixture["teams"]["away"]["name"].replace(" U23", "").replace("W ", "")
    display_date, tz = get_preferred_time_format(date, room, username)
    return f"{away_team} @ {home_team} - {display_date}\n"


def fetch_fox_fixtures(room: str, username: str) -> str:
    """
    Fetch next 5 fixtures played by Foxes.

    :param str room: Chatango room which triggered the command.
    :param str username: Chatango user who triggered the command.

    :returns: str
    """
    try:
        upcoming_foxtures = "\n\n\n:fox: FOXTURES:\n"
        season = datetime.now().year
        params = {"season": season, "team": FOXES_TEAM_ID, "next": "7"}
        params.update(get_preferred_timezone(room, username))
        req = requests.get(
            FOOTY_FIXTURES_ENDPOINT,
            headers=FOOTY_HTTP_HEADERS,
            params=params,
        )
        fixtures = req.json().get("response")
        if bool(fixtures):
            for fixture in fixtures:
                home_team = fixture["teams"]["home"]["name"]
                away_team = fixture["teams"]["away"]["name"]
                date = datetime.strptime(
                    fixture["fixture"]["date"], "%Y-%m-%dT%H:%M:%S%z"
                )
                display_date, tz = get_preferred_time_format(date, room, username)
                if room == CHATANGO_OBI_ROOM:
                    display_date, tz = get_preferred_time_format(date, room, username)
                upcoming_foxtures = (
                    upcoming_foxtures + f"{away_team} @ {home_team} - {display_date}\n"
                )
            return emojize(upcoming_foxtures, use_aliases=True)
        return emojize(
            f":warning: Couldn't find fixtures, has season started yet? :warning:",
            use_aliases=True,
        )
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching fox fixtures: {e.response.content}")
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching fox fixtures: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching fox fixtures: {e}")
