"""Fetch scheduled fixtures across leagues for today only."""
from datetime import datetime
from typing import List, Optional

import requests
from emoji import emojize
from requests.exceptions import HTTPError

from config import FOOTY_FIXTURES_ENDPOINT, FOOTY_HTTP_HEADERS, FOOTY_LEAGUES
from logger import LOGGER

from .util import (
    abbreviate_team_name,
    check_fixture_start_date,
    get_current_day,
    get_preferred_time_format,
    get_preferred_timezone,
    get_season_year,
)


def today_upcoming_fixtures(room: str, username: str) -> str:
    """
    Fetch fixtures scheduled to occur today.

    :param str room: Chatango room in which command was triggered.
    :param str username: Name of user who triggered the command.

    :returns: str
    """
    upcoming_fixtures = "\n\n\n\n"
    i = 0
    for league_name, league_id in FOOTY_LEAGUES.items():
        league_fixtures = today_upcoming_fixtures_per_league(league_name, league_id, room, username)
        if league_fixtures is not None and i < 5:
            i += 1
            upcoming_fixtures += league_fixtures + "\n"
    if upcoming_fixtures != "\n\n\n\n":
        return upcoming_fixtures
    return emojize(
        f":soccer_ball: :cross_mark: sry @{username} no fixtures today :( :cross_mark: :soccer_ball:",
    )


def today_upcoming_fixtures_per_league(
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
        fixtures = fetch_today_fixtures_by_league(league_id, room, username)
        if bool(fixtures) is not False:
            for i, fixture in enumerate(fixtures):
                fixture_start_time = datetime.strptime(
                    fixture["fixture"]["date"], "%Y-%m-%dT%H:%M:%S%z"
                )
                if i == 0 and len(fixture) > 1:
                    league_upcoming_fixtures += emojize(f"<b>{league_name}:</b>\n")
                league_upcoming_fixtures += parse_upcoming_fixture(
                    fixture, fixture_start_time, room, username
                )
            return league_upcoming_fixtures
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching footy fixtures: {e.response.content}")
    except ValueError as e:
        LOGGER.error(f"ValueError while fetching footy fixtures: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching footy fixtures: {e}")


def fetch_today_fixtures_by_league(
    league_id: int, room: str, username: str
) -> List[Optional[dict]]:
    """
    Fetch all upcoming fixtures for the current date.

    :param int league_id: ID of footy league/cup.
    :param str room: Chatango room in which command was triggered.
    :param str username: Name of user who triggered the command.

    :returns: List[Optional[dict]]
    """
    try:
        today = get_current_day(room)
        params = {
            "date": today.strftime("%Y-%m-%d"),
            "league": league_id,
            "status": "NS",
            "season": get_season_year(league_id),
        }
        params.update(get_preferred_timezone(room, username))
        resp = requests.get(
            FOOTY_FIXTURES_ENDPOINT,
            headers=FOOTY_HTTP_HEADERS,
            params=params,
            timeout=20,
        )
        return resp.json().get("response")
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching footy fixtures: {e.response.content}")
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching footy fixtures: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching footy fixtures: {e}")


def parse_upcoming_fixture(
    fixture: dict, fixture_start_time: datetime, room: str, username: str
) -> str:
    """
    Construct upcoming fixture match-up.

    :param dict fixture: Scheduled fixture data.
    :param datetime fixture_start_time: Fixture start time/date displayed in preferred timezone.
    :param str room: Chatango room in which command was triggered.
    :param str username: Name of user who triggered the command.

    :returns: str
    """
    home_team = abbreviate_team_name(fixture["teams"]["home"]["name"])
    away_team = abbreviate_team_name(fixture["teams"]["away"]["name"])
    display_date, tz = get_preferred_time_format(fixture_start_time, room, username)
    display_date = check_fixture_start_date(fixture_start_time, tz, display_date)
    display_date = display_date.replace("Today,", "")
    return f"{away_team} @ {home_team} - {display_date}\n"
