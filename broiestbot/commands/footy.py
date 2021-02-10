"""Footy standings, fixtures, & live games."""
from datetime import datetime
from typing import Optional

import requests
import simplejson as json
from emoji import emojize
from requests.exceptions import HTTPError

from config import CHATANGO_OBI_ROOM, RAPID_API_KEY
from logger import LOGGER


def epl_standings(endpoint: str) -> Optional[str]:
    """
    Get current EPL team standings.

    :param endpoint: Premiere league standings API endpoint.
    :type endpoint: str
    :returns: Optional[str]
    """
    try:
        standings_table = "\n\n"
        headers = {
            "content-type": "application/json",
            "server": "RapidAPI-1.1.0",
            "x-rapidapi-key": RAPID_API_KEY,
            "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
            "x-rapidapi-region": "AWS - eu-central-1",
            "x-rapidapi-version": "1.1.0",
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


def upcoming_epl_fixtures(endpoint: str, room: str) -> Optional[str]:
    """
    Fetch next 10 upcoming EPL fixtures.

    :param endpoint: Upcoming Premiere league fixtures API endpoint.
    :type endpoint: str
    :param room: Chatango room which triggered the command.
    :type room: str
    :returns: Optional[str]
    """
    try:
        upcoming_fixtures = "\n\n"
        params = {"timezone": "America/New_York"}
        headers = {
            "content-type": "application/json",
            "x-rapidapi-key": RAPID_API_KEY,
            "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
        }
        if room == CHATANGO_OBI_ROOM:
            params = {"timezone": "Europe/London"}
        req = requests.get(endpoint, headers=headers, params=params)
        req = json.loads(req.text)
        fixtures = req["api"]["fixtures"]
        for fixture in fixtures:
            home_team = fixture["homeTeam"]["team_name"]
            away_team = fixture["awayTeam"]["team_name"]
            date = datetime.fromtimestamp(fixture["event_timestamp"]).strftime(
                "%b %d %l:%M%p"
            )
            if room == CHATANGO_OBI_ROOM:
                date = datetime.fromtimestamp(fixture["event_timestamp"]).strftime(
                    "%b %d %H:%M"
                )
            upcoming_fixtures = (
                upcoming_fixtures + f"{away_team} @ {home_team} - {date}\n"
            )
        return upcoming_fixtures
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching EPL fixtures: {e.response.content}")
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching EPL fixtures: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching EPL fixtures: {e}")


def live_epl_fixtures(endpoint: str) -> Optional[str]:
    """
    Fetch live EPL fixtures.

    :param endpoint: Live Premiere league fixtures API endpoint.
    :type endpoint: str
    :returns: Optional[str]
    """
    leagues = {"EPL": 2790, "UEFA": 2771, "FA": 2791}
    try:
        live_fixtures = "\n\n\n"
        params = {"timezone": "America/New_York"}
        headers = {
            "content-type": "application/json",
            "x-rapidapi-key": RAPID_API_KEY,
            "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
        }
        req = requests.get(endpoint, headers=headers, params=params)
        fixtures = json.loads(req.text)["api"]["fixtures"]
        leagues = [league for league in leagues.values()]
        for league in leagues:
            fixtures = [
                fixture for fixture in fixtures if fixture["league_id"] == league
            ]
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


def all_live_fixtures(endpoint: str) -> Optional[str]:
    """
    Fetch live EPL fixtures.

    :param endpoint: Live Premiere league fixtures API endpoint.
    :type endpoint: str
    :returns: Optional[str]
    """
    leagues = {"EPL": 2790, "UEFA": 2771, "FA": 2791}
    try:
        live_fixtures = "\n\n\n"
        params = {"timezone": "America/New_York"}
        headers = {
            "content-type": "application/json",
            "x-rapidapi-key": RAPID_API_KEY,
            "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
        }
        req = requests.get(
            f"https://api-football-v1.p.rapidapi.com/v2/fixtures/live/{leagues['EPL']}-{leagues['UEFA']}-{leagues['FA']}",
            headers=headers,
            params=params,
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


def golden_boot():
    golden_boot_leaders = "\n\n\n"
    headers = {
        "content-type": "application/json",
        "x-rapidapi-key": RAPID_API_KEY,
        "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
    }
    try:
        req = requests.get(
            f"https://api-football-v1.p.rapidapi.com/v2/topscorers/2790",
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
            golden_boot_leaders += f"{name}, {team}. {goals} goals, {assists} assists, {shots_on}/{shots_total}\n"
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
