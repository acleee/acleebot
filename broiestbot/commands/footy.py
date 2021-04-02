"""Footy standings, fixtures, live games, scoring leaders, & predicts."""
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import pytz
import requests
import simplejson as json
from emoji import emojize
from requests.exceptions import HTTPError

from config import (
    CHATANGO_OBI_ROOM,
    FOOTY_LEAGUE_IDS,
    METRIC_SYSTEM_USERS,
    RAPID_API_KEY,
)
from logger import LOGGER


def epl_standings(endpoint: str) -> Optional[str]:
    """
    Get standings table for EPL.

    :param endpoint: Premiere league standings API endpoint.
    :type endpoint: str
    :returns: Optional[str]
    """
    try:
        standings_table = "\n\n"
        headers = {
            "content-type": "application/json",
            "x-rapidapi-key": RAPID_API_KEY,
            "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
        }
        req = requests.get(endpoint, headers=headers)
        req = json.loads(req.text)
        standings = req["api"]["standings"][0]
        for standing in standings:
            rank = standing["rank"]
            team = standing["teamName"]
            points = standing["points"]
            wins = standing["all"]["win"]
            draws = standing["all"]["draw"]
            losses = standing["all"]["lose"]
            standings_table = (
                standings_table
                + f"{rank}. {team}: {points}pts ({wins}-{draws}-{losses})\n"
            )
        return standings_table
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching EPL standings: {e.response.content}")
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching EPL standings: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching EPL standings: {e}")


def footy_upcoming_fixtures(room: str, username: str) -> str:
    """
    Fetch upcoming fixtures within 1 week for EPL, LIGA, BUND, FA, UCL, and EUROPA.

    :param room: Chatango room where command was triggered.
    :type room: str
    :param username: Chatango user who triggered the command.
    :type username: str
    :returns: str
    """
    upcoming_fixtures = "\n\n"
    for league_name, league_id in FOOTY_LEAGUE_IDS.items():
        league_fixtures = footy_upcoming_fixtures_per_league(
            league_name, league_id, room, username
        )
        if league_fixtures is not None:
            upcoming_fixtures += league_fixtures + "\n"
    return upcoming_fixtures


def footy_upcoming_fixtures_per_league(
    league_name: str, league_id: int, room: str, username: str
) -> Optional[str]:
    """
    Get upcoming fixtures for a given league.

    :param league_name: Name of footy league.
    :type league_name: str
    :param league_id: ID of footy league.
    :type league_id: int
    :param room: Chatango room which triggered the command.
    :type room: str
    :param username: Chatango user who triggered the command.
    :type username: str
    :returns: Optional[str]
    """
    try:
        num_fixtures = 0
        upcoming_fixtures = ""
        params = get_preferred_timezone(room, username)
        headers = {
            "content-type": "application/json",
            "x-rapidapi-key": RAPID_API_KEY,
            "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
        }
        req = requests.get(
            f"https://api-football-v1.p.rapidapi.com/v2/fixtures/league/{league_id}/next/5/",
            headers=headers,
            params=params,
        )
        req = json.loads(req.text)
        fixtures = req["api"]["fixtures"]
        if bool(fixtures):
            for i, fixture in enumerate(fixtures):
                home_team = fixture["homeTeam"]["team_name"]
                away_team = fixture["awayTeam"]["team_name"]
                date = datetime.strptime(fixture["event_date"], "%Y-%m-%dT%H:%M:%S%z")
                display_date = get_preferred_time_format(date, room, username)
                tz = get_preferred_timezone_object(room, username)
                if date - datetime.now(tz=tz) < timedelta(days=7):
                    if room == CHATANGO_OBI_ROOM:
                        display_date = get_preferred_time_format(date, room, username)
                    num_fixtures += 1
                    if num_fixtures > 0:
                        if num_fixtures == 1:
                            upcoming_fixtures += f"{league_name}:\n"
                    upcoming_fixtures = (
                        upcoming_fixtures
                        + f"{away_team} @ {home_team} - {display_date}\n"
                    )
            return upcoming_fixtures
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching footy fixtures: {e.response.content}")
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching footy fixtures: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching footy fixtures: {e}")


def footy_live_fixtures() -> Optional[str]:
    """
    Fetch live footy fixtures across EPL, LIGA, BUND, FA, UCL, and EUROPA.

    :returns: Optional[str]
    """
    try:
        live_fixtures = "\n\n\n"
        headers = {
            "content-type": "application/json",
            "x-rapidapi-key": RAPID_API_KEY,
            "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
        }
        leagues = f"{FOOTY_LEAGUE_IDS['EPL']}-{FOOTY_LEAGUE_IDS['UCL']}-{FOOTY_LEAGUE_IDS['FA']}-{FOOTY_LEAGUE_IDS['EUROPA']}-{FOOTY_LEAGUE_IDS['BUND']}-{FOOTY_LEAGUE_IDS['LIGA']}"
        req = requests.get(
            f"https://api-football-v1.p.rapidapi.com/v2/fixtures/live/{leagues}",
            headers=headers,
        )
        fixtures = req.json()["api"]["fixtures"]
        if bool(fixtures):
            for i, fixture in enumerate(fixtures):
                home_team = fixture["homeTeam"]["team_name"]
                away_team = fixture["awayTeam"]["team_name"]
                home_score = fixture["goalsHomeTeam"]
                away_score = fixture["goalsAwayTeam"]
                elapsed = fixture["elapsed"]
                venue = fixture["venue"]
                events = fixture.get("events")
                live_fixtures = (
                    live_fixtures
                    + f'{home_team} {home_score} - {away_team} {away_score}\n{venue}, {elapsed}"\n'
                )
                if events:
                    for event in events:
                        if event["detail"] == "Yellow Card":
                            live_fixtures = live_fixtures + emojize(
                                f':yellow_square: {event["detail"]}, {event["player"]} {event["elapsed"]}"\n'
                            )
                        elif event["detail"] == "Red Card":
                            live_fixtures = live_fixtures + emojize(
                                f':red_square: {event["detail"]}, {event["player"]} {event["elapsed"]}"\n'
                            )
                        elif event["type"] == "Goal":
                            live_fixtures = live_fixtures + emojize(
                                f':soccer_ball: {event["type"]}, {event["player"]} {event["elapsed"]}"\n'
                            )
                        elif event["type"] == "subst":
                            live_fixtures = live_fixtures + emojize(
                                f':red_triangle_pointed_down: {event["detail"]} :evergreen_tree: {event["player"]} {event["elapsed"]}"\n'
                            )
                if i < len(fixtures) - 1:
                    live_fixtures = live_fixtures + "-------------------------\n"
            return live_fixtures
        return "No live fixtures :("
    except HTTPError as e:
        LOGGER.error(
            f"HTTPError while fetching live EPL fixtures: {e.response.content}"
        )
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching live EPL fixtures: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching live EPL fixtures: {e}")


def epl_golden_boot() -> str:
    """
    Get EPL top scorers.

    :return: str
    """
    golden_boot_leaders = "\n\n\n"
    headers = {
        "content-type": "application/json",
        "x-rapidapi-key": RAPID_API_KEY,
        "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
    }
    try:
        req = requests.get(
            f"https://api-football-v1.p.rapidapi.com/v2/topscorers/{FOOTY_LEAGUE_IDS['EPL']}",
            headers=headers,
        )
        players = req.json()["api"]["topscorers"]
        for i, player in enumerate(players):
            name = player["player_name"]
            team = player["team_name"]
            goals = player["goals"]["total"]
            assists = player["goals"]["assists"]
            shots_on = player["shots"]["on"]
            shots_total = player["shots"]["total"]
            golden_boot_leaders += f"{goals} - {name}, {team}. ({assists} assists, {shots_on}/{shots_total} SOG)\n"
            if i > 9:
                break
        return golden_boot_leaders
    except HTTPError as e:
        LOGGER.error(
            f"HTTPError while fetching golden boot leaders: {e.response.content}"
        )
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching golden boot leaders: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching golden boot leaders: {e}")


def footy_predicts_today(room: str, username: str) -> Optional[str]:
    """
    Fetch odds for fixtures being played today.

    :param room: Chatango room which triggered the command.
    :type room: str
    :param username: Chatango user who triggered the command.
    :type username: str
    :returns: Optional[str]
    """
    todays_predicts = "\n\n\n"
    try:
        fixture_ids = footy_fixtures_today(room, username)
        if bool(fixture_ids) is False:
            return "No fixtures today :("
        for fixture_id in fixture_ids:
            url = f"https://api-football-v1.p.rapidapi.com/v2/predictions/{fixture_id}"
            headers = {
                "x-rapidapi-key": "g0WO10fWOCmshLudRLxChsXgQlCtp15tFmkjsn5qiWhSv1HcPs",
                "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
            }
            res = requests.get(url, headers=headers)
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


def footy_fixtures_today(room: str, username: str) -> List[int]:
    """
    Gets fixture IDs of fixtures being played today.

    :param room: Chatango room which triggered the command.
    :type room: str
    :param username: Chatango user who triggered the command.
    :type username: str
    :returns: List[int]
    """
    try:
        today = datetime.now().date()
        url = f"https://api-football-v1.p.rapidapi.com/v2/fixtures/date/{today}"
        params = get_preferred_timezone(room, username)
        headers = {
            "x-rapidapi-key": "g0WO10fWOCmshLudRLxChsXgQlCtp15tFmkjsn5qiWhSv1HcPs",
            "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
        }
        res = requests.get(url, headers=headers, params=params)
        fixtures = res.json()["api"]["fixtures"]
        if bool(fixtures):
            return [
                fixture["fixture_id"]
                for fixture in fixtures
                if fixture["league_id"] in FOOTY_LEAGUE_IDS.values()
            ]
    except HTTPError as e:
        LOGGER.error(
            f"HTTPError while fetching today's footy fixtures: {e.response.content}"
        )
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching today's footy fixtures: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching today's footy fixtures: {e}")


def get_preferred_timezone(room: str, username: str) -> Dict:
    """
    Display fixture dates depending on preferred timezone of requesting user.

    :param room: Chatango room which triggered the command.
    :type room: str
    :param username: Chatango user who triggered the command.
    :type username: str
    :returns: str
    """
    if room == CHATANGO_OBI_ROOM or username in METRIC_SYSTEM_USERS:
        return {}
    return {"timezone": "America/New_York"}


def get_preferred_time_format(start_time: datetime, room: str, username: str):
    """
    Display fixture times depending on preferred timezone of requesting user.

    :param start_time: Unformatted fixture start time/date.
    :type start_time: datetime
    :param room: Chatango room which triggered the command.
    :type room: str
    :param username: Chatango user who triggered the command.
    :type username: str
    :returns: str
    """
    if room == CHATANGO_OBI_ROOM or username in METRIC_SYSTEM_USERS:
        return start_time.strftime("%b %d, %H:%M")
    return start_time.strftime("%b %d, %l:%M%p").replace("AM", "am").replace("PM", "pm")


def get_preferred_timezone_object(room: str, username: str):
    """
    Display fixture dates depending on preferred timezone of requesting user.

    :param room: Chatango room which triggered the command.
    :type room: str
    :param username: Chatango user who triggered the command.
    :type username: str
    :returns: str
    """
    if room == CHATANGO_OBI_ROOM or username in METRIC_SYSTEM_USERS:
        return pytz.utc
    return pytz.timezone("America/New_York")
