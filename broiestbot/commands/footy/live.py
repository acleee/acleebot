"""Match breakdown of all live fixtures."""
from typing import Optional

import requests
from emoji import emojize
from requests.exceptions import HTTPError

from config import (
    FOOTY_FIXTURES_ENDPOINT,
    FOOTY_HTTP_HEADERS,
    FOOTY_LEAGUES,
    FOOTY_LIVE_FIXTURE_EVENTS_ENDPOINT,
    HTTP_REQUEST_TIMEOUT,
)
from logger import LOGGER

from .util import get_preferred_timezone


def footy_live_fixtures(room: str, username: str, subs=False) -> str:
    """
    Fetch live fixtures for EPL, LIGA, BUND, FA, UCL, EUROPA, etc.

    :param str room: Chatango room in which command was triggered.
    :param str username: Name of user who triggered the command.
    :param bool subs: Whether to include substitutions in match summaries.

    :returns: str
    """
    live_fixtures = "\n\n\n\n"
    i = 0
    for league_name, league_id in FOOTY_LEAGUES.items():
        live_league_fixtures = footy_live_fixtures_per_league(
            league_id, league_name, room, username, subs=subs
        )
        if live_league_fixtures is not None and i < 6:
            i += 1
            live_fixtures += live_league_fixtures + "\n"
    if live_fixtures == "\n\n\n\n":
        return emojize(":warning: No live fixtures :( :warning:")
    return live_fixtures


def footy_live_fixtures_per_league(
    league_id: int, league_name: str, room: str, username: str, subs=False
) -> Optional[str]:
    """
    Construct summary of events for all live fixtures in a given league.

    :param int league_id: ID of footy league/cup.
    :param str league_name: Name of league or cup fixtures belong to.
    :param str room: Chatango room in which command was triggered.
    :param str username: Name of user who triggered the command.
    :param bool subs: Whether to include substitutions in match summaries.

    :returns: Optional[str]
    """
    try:
        live_fixtures = "\n\n\n\n"
        fixtures = fetch_live_fixtures(league_id, room, username)
        if fixtures:
            live_fixtures += emojize(f"<b>{league_name}:</b>\n")
            for i, fixture in enumerate(fixtures):
                home_team = fixture["teams"]["home"]["name"]
                away_team = fixture["teams"]["away"]["name"]
                home_score = fixture["goals"]["home"]
                away_score = fixture["goals"]["away"]
                elapsed = fixture["fixture"]["status"]["elapsed"]
                venue = fixture["fixture"]["venue"]["name"]
                live_fixture = f'<b>{home_team} {home_score} - {away_team} {away_score}</b>\n{venue}, {elapsed}"'
                live_fixtures += live_fixture
                events = get_events_per_live_fixture(fixture["fixture"]["id"], subs=subs)
                if events:
                    live_fixtures += events
                if i < len(fixtures):
                    live_fixtures += "\n\n\n"
            if live_fixtures != "\n\n\n\n":
                return live_fixtures
        return None
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching live fixtures: {e.response.content}")
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching live fixtures: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching live fixtures: {e}")


def fetch_live_fixtures(league_id: int, room: str, username: str) -> Optional[str]:
    """
    Fetch live footy fixtures across EPL, LIGA, BUND, FA, UCL, EUROPA, etc.

    :param int league_id: ID of footy league/cup.
    :param str room: Chatango room in which command was triggered.
    :param str username: Name of user who triggered the command.

    :returns: Optional[str]
    """
    try:
        params = {"league": league_id, "live": "all"}
        params.update(get_preferred_timezone(room, username))
        res = requests.get(
            FOOTY_FIXTURES_ENDPOINT,
            headers=FOOTY_HTTP_HEADERS,
            params=params,
            timeout=HTTP_REQUEST_TIMEOUT,
        )
        return res.json().get("response")
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching footy fixtures: {e.response.content}")
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching footy fixtures: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching footy fixtures: {e}")


def get_events_per_live_fixture(fixture_id: int, subs=False) -> Optional[str]:
    """
    Construct timeline of events for a single live fixture.

    :param int fixture_id: ID of a single live fixture.
    :param bool subs: Whether to include substitutions in match summaries.

    :returns: Optional[str]
    """
    try:
        event_log = "\n"
        params = {"fixture": fixture_id}
        req = requests.get(
            FOOTY_LIVE_FIXTURE_EVENTS_ENDPOINT,
            headers=FOOTY_HTTP_HEADERS,
            params=params,
            timeout=HTTP_REQUEST_TIMEOUT,
        )
        events = req.json().get("response")
        if events:
            for i, event in enumerate(events):
                if event["detail"] == "Yellow Card":
                    event_log = event_log + emojize(
                        f':yellow_square: {event["player"]["name"]} {event["time"]["elapsed"]}"\n',
                    )
                elif event["detail"] == "Second Yellow card":
                    event_log = event_log + emojize(
                        f':yellow_square::yellow_square: {event["player"]["name"]} {event["time"]["elapsed"]}"\n',
                    )
                elif event["detail"] == "Red Card":
                    event_log = event_log + emojize(
                        f':red_square: {event["player"]["name"]} {event["time"]["elapsed"]}"\n',
                    )
                elif event["detail"] == "Normal Goal":
                    event_log = event_log + emojize(
                        f':soccer_ball: {event["type"]}, {event["player"]["name"]} {event["time"]["elapsed"]}"\n',
                    )
                elif event["detail"] == "Penalty":
                    event_log = event_log + emojize(
                        f':goal_net: :soccer_ball: (PEN), {event["player"]["name"]} {event["time"]["elapsed"]}"\n',
                    )
                elif event["detail"] == "Own Goal":
                    event_log = event_log + emojize(
                        f':skull: :soccer_ball: {event["player"]["name"]} (via {event["assist"]["name"]}) {event["time"]["elapsed"]}"\n',
                    )
                elif event["type"] == "subst" and subs is True:
                    event_log = event_log + emojize(
                        f':red_triangle_pointed_down: {event["assist"]["name"]} :evergreen_tree: {event["player"]["name"]} {event["time"]["elapsed"]}"\n',
                    )
            return event_log
        return None
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching live fixtures: {e.response.content}")
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching live fixtures: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching live fixtures: {e}")
