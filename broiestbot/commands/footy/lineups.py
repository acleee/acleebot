"""Fetch lineups before kickoff or during the match."""
import requests
from emoji import emojize

from config import FOOTY_HTTP_HEADERS, FOOTY_LEAGUES_LINEUPS, FOOTY_XI_ENDPOINT

from .today import todays_upcoming_fixtures_by_league


def footy_team_lineups(room: str, username: str) -> str:
    """
    Fetch starting lineups by team for immediate or live fixtures.

    :param str room: Chatango room in which command was triggered.
    :param str username: Name of user who triggered the command.

    :returns: str
    """
    todays_fixture_lineups = "\n\n\n\n"
    for league_name, league_id in FOOTY_LEAGUES_LINEUPS.items():
        todays_fixtures = todays_upcoming_fixtures_by_league(league_id, room, username)
        if bool(todays_fixtures):
            for fixture in todays_fixtures:
                todays_fixture_lineups += get_xi_per_fixture_team(fixture["id"])
            return todays_fixture_lineups
    return emojize(":warning: Couldn't find any upcoming fixtures :( :warning:", use_aliases=True)


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
