"""Footy standings, fixtures, live games, scoring leaders, & predicts."""
from datetime import datetime, timedelta
from typing import List, Optional, Tuple

import pytz
import requests
import simplejson as json
from emoji import emojize
from pytz import BaseTzInfo
from requests.exceptions import HTTPError

from config import (
    CHATANGO_OBI_ROOM,
    FOOTY_LEAGUE_IDS,
    METRIC_SYSTEM_USERS,
    RAPID_API_KEY,
)
from logger import LOGGER

headers = {
    "content-type": "application/json",
    "x-rapidapi-key": RAPID_API_KEY,
    "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
}


def epl_standings(endpoint: str) -> Optional[str]:
    """
    Get team standings table for EPL.

    :param endpoint: Premiere league standings API endpoint.
    :type endpoint: str
    :returns: Optional[str]
    """
    try:
        standings_table = "\n\n"
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


def liga_standings(endpoint: str) -> Optional[str]:
    """
    Get standings table for La Liga.

    :param str endpoint: La Liga standings API endpoint.

    :returns: Optional[str]
    """
    try:
        standings_table = "\n\n"
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
        LOGGER.error(f"HTTPError while fetching LIGA standings: {e.response.content}")
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching LIGA standings: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching LIGA standings: {e}")


def bund_standings(endpoint: str) -> Optional[str]:
    """
    Get standings table for Bundesliga.

    :param str endpoint: Bundesliga standings API endpoint.

    :returns: Optional[str]
    """
    try:
        standings_table = "\n\n"
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
        LOGGER.error(f"HTTPError while fetching BUND standings: {e.response.content}")
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching BUND standings: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching BUND standings: {e}")


def footy_upcoming_fixtures(room: str, username: str) -> str:
    """
    Fetch upcoming fixtures within 1 week for EPL, LIGA, BUND, FA, UCL, EUROPA, etc.

    :param str room: Chatango room in which command was triggered.
    :param str username: Name of user who triggered the command.

    :returns: str
    """
    upcoming_fixtures = "\n\n"
    for league_name, league_id in FOOTY_LEAGUE_IDS.items():
        league_fixtures = footy_upcoming_fixtures_per_league(
            league_name, league_id, room, username
        )
        if league_fixtures is not None:
            upcoming_fixtures += league_fixtures + "\n"
    if upcoming_fixtures != "\n\n":
        return upcoming_fixtures
    return emojize(":warning: Couldn't find any upcoming fixtures :warning:")


def footy_upcoming_fixtures_per_league(
    league_name: str, league_id: int, room: str, username: str
) -> Optional[str]:
    """
    Get upcoming fixtures for a given league or tournament.

    :param str league_name: Name of footy league/cup.
    :param int league_id: ID of footy league/cup.
    :param str room: Chatango room in which command was triggered.
    :param str username: Name of user who triggered the command.

    :returns: Optional[str]
    """
    try:
        upcoming_fixtures = ""
        season = datetime.now().year
        fixtures = fetch_upcoming_fixtures(season, league_id, room, username)
        if bool(fixtures) is False:
            fixtures = fetch_upcoming_fixtures(season - 1, league_id, room, username)
        if fixtures and len(fixtures) > 0:
            for i, fixture in enumerate(fixtures):
                date = datetime.strptime(
                    fixture["fixture"]["date"], "%Y-%m-%dT%H:%M:%S%z"
                )
                display_date, tz = get_preferred_time_format(date, room, username)
                if room == CHATANGO_OBI_ROOM:
                    display_date, tz = get_preferred_time_format(date, room, username)
                if date - datetime.now(tz=tz) < timedelta(days=10):
                    if i == 0:
                        upcoming_fixtures += emojize(f"{league_name}:\n")
                    home_team = fixture["teams"]["home"]["name"]
                    away_team = fixture["teams"]["away"]["name"]
                    display_date, tz = get_preferred_time_format(date, room, username)
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


def footy_live_fixtures(room: str, username: str) -> str:
    """
    Fetch live fixtures for EPL, LIGA, BUND, FA, UCL, EUROPA, etc.

    :param str room: Chatango room in which command was triggered.
    :param str username: Name of user who triggered the command.

    :returns: str
    """
    live_fixtures = "\n\n\n"
    for league_name, league_id in FOOTY_LEAGUE_IDS.items():
        league_fixtures = footy_live_fixtures_per_league(league_id, room, username)
        if league_fixtures is not None:
            live_fixtures += league_fixtures + "\n"
    if live_fixtures == "\n\n\n":
        return ":warning: No live fixtures :( :warning:"
    return live_fixtures


def fetch_upcoming_fixtures(season: int, league_id: int, room: str, username: str):
    """
    Fetch next 5 upcoming fixtures for a given league.

    :param int season: Season year of league/cup.
    :param int league_id: ID of footy league/cup.
    :param str room: Chatango room in which command was triggered.
    :param str username: Name of user who triggered the command.
    """
    try:
        params = {"season": season, "league": league_id, "next": 5, "status": "NS"}
        params.update(get_preferred_timezone(room, username))
        req = requests.get(
            f"https://api-football-v1.p.rapidapi.com/v3/fixtures",
            headers=headers,
            params=params,
        )
        return req.json().get("response")
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching footy fixtures: {e.response.content}")
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching footy fixtures: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching footy fixtures: {e}")


def footy_live_fixtures_per_league(
    league_id: int, room: str, username: str
) -> Optional[str]:
    """
    Construct summary of events for all live fixtures in a given league.

    :param int league_id: ID of footy league/cup.
    :param str room: Chatango room in which command was triggered.
    :param str username: Name of user who triggered the command.

    :returns: Optional[str]
    """
    try:
        live_fixtures = "\n\n"
        season = datetime.now().year
        fixtures = fetch_live_fixtures(season, league_id, room, username)
        if bool(fixtures) is False or fixtures is None:
            fixtures = fetch_live_fixtures(season - 1, league_id, room, username)
        if fixtures:
            for i, fixture in enumerate(fixtures):
                home_team = fixture["teams"]["home"]["name"]
                away_team = fixture["teams"]["away"]["name"]
                home_score = fixture["goals"]["home"]
                away_score = fixture["goals"]["away"]
                elapsed = fixture["fixture"]["status"]["elapsed"]
                venue = fixture["fixture"]["venue"]["name"]
                live_fixtures = (
                    live_fixtures
                    + f'{home_team} {home_score} - {away_team} {away_score}\n{venue}, {elapsed}"\n'
                )
                events = get_events_per_live_fixture(fixture["fixture"]["id"])
                if events:
                    live_fixtures = live_fixtures + events
                    if i < len(fixtures) - 1 and len(fixtures) > 1:
                        live_fixtures = live_fixtures + "——————————————————\n"
                    return live_fixtures
        return None
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching live fixtures: {e.response.content}")
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching live fixtures: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching live fixtures: {e}")


def fetch_live_fixtures(
    season: int, league_id: int, room: str, username: str
) -> Optional[str]:
    """
    Fetch live footy fixtures across EPL, LIGA, BUND, FA, UCL, EUROPA, etc.

    :param int season: Season year of league/cup.
    :param int league_id: ID of footy league/cup.
    :param str room: Chatango room in which command was triggered.
    :param str username: Name of user who triggered the command.

    :returns: Optional[str]
    """
    try:

        params = {"season": season, "league": league_id, "live": "all"}
        params.update(get_preferred_timezone(room, username))
        req = requests.get(
            f"https://api-football-v1.p.rapidapi.com/v3/fixtures",
            headers=headers,
            params=params,
        )
        return req.json().get("response")
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching footy fixtures: {e.response.content}")
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching footy fixtures: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching footy fixtures: {e}")


def get_events_per_live_fixture(fixture_id: int) -> Optional[str]:
    """
    Construct timeline of events for a single live fixture.

    :param int fixture_id: ID of a single live fixture.

    :returns: Optional[str]
    """
    try:
        event_log = "\n\n"
        params = {"fixture": fixture_id}
        req = requests.get(
            "https://api-football-v1.p.rapidapi.com/v3/fixtures/events",
            headers=headers,
            params=params,
        )
        events = req.json().get("response")
        if events:
            for i, event in enumerate(events):
                if event["detail"] == "Yellow Card":
                    event_log = event_log + emojize(
                        f':yellow_square: {event["detail"]}, {event["player"]["name"]} {event["time"]["elapsed"]}"\n'
                    )
                elif event["detail"] == "Second Yellow card":
                    event_log = event_log + emojize(
                        f':yellow_square::yellow_square: {event["detail"]}, {event["player"]["name"]} {event["time"]["elapsed"]}"\n'
                    )
                elif event["detail"] == "Red Card":
                    event_log = event_log + emojize(
                        f':red_square: {event["detail"]}, {event["player"]["name"]} {event["time"]["elapsed"]}"\n'
                    )
                elif event["detail"] == "Normal Goal":
                    event_log = event_log + emojize(
                        f':soccer_ball: {event["type"]}, {event["player"]["name"]} {event["time"]["elapsed"]}"\n'
                    )
                elif event["detail"] == "Own Goal":
                    event_log = event_log + emojize(
                        f':skull: :soccer_ball: {event["type"]}, {event["player"]["name"]} (via {event["assist"]["name"]}) {event["time"]["elapsed"]}"\n'
                    )
                elif event["type"] == "subst":
                    event_log = event_log + emojize(
                        f':red_triangle_pointed_down: {event["assist"]["name"]} :evergreen_tree: {event["player"]["name"]} {event["time"]["elapsed"]}"\n'
                    )
            return event_log
        return None
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching live fixtures: {e.response.content}")
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching live fixtures: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching live fixtures: {e}")


def epl_golden_boot() -> str:
    """
    Fetch list of EPL golden boot top scorers.

    :return: str
    """
    golden_boot_leaders = "\n\n\n"
    try:
        season = datetime.now().year
        params = {"season": season, "league": 39}
        req = requests.get(
            "https://api-football-v1.p.rapidapi.com/v3/players/topscorers",
            headers=headers,
            params=params,
        )
        players = req.json().get("response")
        if players:
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
        return f":warning: Couldn't find golden boot leaders; has season started yet? :warning:"
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
            url = f"https://api-football-v1.p.rapidapi.com/v3/predictions/{fixture_id}"
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
        url = f"https://api-football-v1.p.rapidapi.com/v3/fixtures"
        params = {"date": display_date}
        params.update(get_preferred_timezone(room, username))
        res = requests.get(url, headers=headers, params=params)
        fixtures = res.json().get("response")
        if bool(fixtures):
            return [
                fixture["fixture"]["id"]
                for fixture in fixtures
                if fixture["league"]["id"] in FOOTY_LEAGUE_IDS.values()
            ]
    except HTTPError as e:
        LOGGER.error(
            f"HTTPError while fetching today's footy fixtures: {e.response.content}"
        )
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching today's footy fixtures: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching today's footy fixtures: {e}")


def get_fox_fixtures(room: str, username: str) -> str:
    """
    Fetch next 5 fixtures played by Foxes.

    :param str room: Chatango room which triggered the command.
    :param str username: Chatango user who triggered the command.

    :returns: str
    """
    try:
        upcoming_foxtures = "\n\n\n:fox: FOXTURES:\n"
        season = datetime.now().year
        params = {"season": season, "team": "46", "next": "7"}
        params.update(get_preferred_timezone(room, username))
        req = requests.get(
            "https://api-football-v1.p.rapidapi.com/v3/fixtures",
            headers=headers,
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
            return emojize(upcoming_foxtures)
        return f":warning: Couldn't find fixtures, has season started yet? :warning:"
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching footy fixtures: {e.response.content}")
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching footy fixtures: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching footy fixtures: {e}")


def get_preferred_timezone(room: str, username: str) -> dict:
    """
    Display fixture dates depending on preferred timezone of requesting user.

    :param str room: Chatango room which triggered the command.
    :param str username: Chatango user who triggered the command.

    :returns: dict
    """
    if room == CHATANGO_OBI_ROOM or username in METRIC_SYSTEM_USERS:
        return {}
    return {"timezone": "America/New_York"}


def get_preferred_time_format(
    start_time: datetime, room: str, username: str
) -> Tuple[str, BaseTzInfo]:
    """
    Display fixture times depending on preferred timezone of requesting user/room.

    :param datetime start_time: Fixture start time/date defaulted to UTC time.
    :param str room: Chatango room in which command was triggered.
    :param str username: Name of user who triggered the command.

    :returns: Tuple[str, BaseTzInfo]
    """
    if room == CHATANGO_OBI_ROOM or username in METRIC_SYSTEM_USERS:
        return start_time.strftime("%b %d, %H:%M"), pytz.utc
    return (
        start_time.strftime("%b %d, %l:%M%p").replace("AM", "am").replace("PM", "pm"),
        pytz.timezone("America/New_York"),
    )
