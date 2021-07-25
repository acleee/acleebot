"""Match breakdown of all currently live fixtures."""
from datetime import datetime
from typing import List, Optional

import requests
from requests.exceptions import HTTPError

from config import (
    FOOTY_LEAGUES_BY_SEASON,
    RAPID_FOOTY_FIXTURES_ENDPOINT,
    RAPID_FOOTY_PREDICTS_ENDPOINT,
    RAPID_HTTP_HEADERS,
)
from logger import LOGGER

from .util import get_preferred_time_format, get_preferred_timezone


def footy_predicts_today(room: str, username: str) -> Optional[str]:
    """
    Fetch odds for fixtures being played today.

    :param str room: Chatango room which triggered the command.
    :param str username: Chatango user who triggered the command.

    :returns: Optional[str]
    """
    todays_predicts = "\n\n\n"
    try:
        fixture_ids = footy_fixtures_today(room, username)
        if bool(fixture_ids) is False:
            return "No fixtures today :("
        for fixture_id in fixture_ids:
            url = f"{RAPID_FOOTY_PREDICTS_ENDPOINT}/{fixture_id}"
            res = requests.get(url, headers=RAPID_HTTP_HEADERS)
            predictions = res.json()["api"]["predictions"]
            for prediction in predictions:
                home_chance = prediction["winning_percent"]["home"]
                away_chance = prediction["winning_percent"]["away"]
                draw_chance = prediction["winning_percent"]["draws"]
                home_name = prediction["teams"]["home"]["team_name"]
                away_name = prediction["teams"]["away"]["team_name"]
                todays_predicts = (
                    todays_predicts
                    + f"{away_name} {away_chance} @ {home_name} {home_chance} (draw {draw_chance})\n"
                )
        return todays_predicts
    except HTTPError as e:
        LOGGER.error(
            f"HTTPError while fetching today's footy predicts: {e.response.content}"
        )
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching today's footy predicts: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching today's footy predicts: {e}")


def footy_fixtures_today(room: str, username: str) -> Optional[List[int]]:
    """
    Gets fixture IDs of fixtures being played today.

    :param str room: Chatango room which triggered the command.
    :param str username: Chatango user who triggered the command.

    :returns: Optional[List[int]]
    """
    try:
        today = datetime.now()
        display_date, tz = get_preferred_time_format(today, room, username)
        params = {"date": display_date}
        params.update(get_preferred_timezone(room, username))
        res = requests.get(
            RAPID_FOOTY_FIXTURES_ENDPOINT, headers=RAPID_HTTP_HEADERS, params=params
        )
        fixtures = res.json().get("response")
        if bool(fixtures):
            return [
                fixture["fixture"]["id"]
                for fixture in fixtures
                if fixture["league"]["id"] in FOOTY_LEAGUES_BY_SEASON.values()
            ]
    except HTTPError as e:
        LOGGER.error(
            f"HTTPError while fetching today's footy fixtures: {e.response.content}"
        )
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching today's footy fixtures: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching today's footy fixtures: {e}")
