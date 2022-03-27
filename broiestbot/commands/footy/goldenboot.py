"""Top scorers for a given league."""
from datetime import datetime
from typing import List, Tuple

import requests
from emoji import emojize
from requests.exceptions import HTTPError

from config import (
    EPL_LEAGUE_ID,
    FOOTY_HTTP_HEADERS,
    FOOTY_TOPSCORERS_ENDPOINT,
    GOLDEN_SHOE_LEAGUES,
)
from logger import LOGGER

from .util import get_season_year


def epl_golden_boot() -> str:
    """
    Construct list of EPL top scorers.

    :return: str
    """
    try:
        top_scorers = []
        top_scorers.extend(golden_boot_leaders(league=EPL_LEAGUE_ID))
        if bool(top_scorers):
            top_scorers.sort(key=lambda x: x[0], reverse=True)
            top_scorers = top_scorers[:20]
            top_scorers = [scorer[1] for scorer in top_scorers]
            top_scorers.insert(0, "\n\n\n\n")
            return "\n".join(top_scorers)
        return emojize(
            f":warning: Couldn't find golden boot leaders; bot is shit tbh :warning:",
            use_aliases=True,
        )
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching golden boot leaders: {e}")


def all_leagues_golden_boot() -> str:
    """
    Fetch list of top scorers per league.

    :return: str
    """
    try:
        top_scorers = []
        for league_id in GOLDEN_SHOE_LEAGUES.values():
            top_scorers.extend(golden_boot_leaders(league=league_id))
        if bool(top_scorers):
            top_scorers.sort(key=lambda x: x[0], reverse=True)
            top_scorers = top_scorers[:20]
            top_scorers = [scorer[1] for scorer in top_scorers]
            top_scorers.insert(0, "\n\n\n\n")
            return "\n".join(top_scorers)
        return emojize(
            f":warning: Couldn't find golden boot shoe; bot is shit tbh :warning:",
            use_aliases=True,
        )
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching golden shoe leaders: {e}")


def golden_boot_leaders(league=EPL_LEAGUE_ID) -> List[Tuple[int, str]]:
    """
    Fetch list of top scorers per league.

    :return: List[str]
    """
    try:
        top_scorers = []
        season = get_season_year(EPL_LEAGUE_ID)
        params = {"season": season, "league": league}
        req = requests.get(
            FOOTY_TOPSCORERS_ENDPOINT,
            headers=FOOTY_HTTP_HEADERS,
            params=params,
        )
        players = req.json().get("response")
        if players:
            for i, player in enumerate(players):
                name = player["player"]["name"]
                team = player["statistics"][0]["team"]["name"]
                goals = player["statistics"][0]["goals"]["total"]
                assists = player["statistics"][0]["goals"].get("assists", 0)
                shots_on = player["statistics"][0]["shots"].get("on", 0)
                shots_total = player["statistics"][0]["shots"].get("total", 0)
                if assists is None:
                    assists = 0
                top_scorers.append(
                    (
                        goals,
                        f"{goals} - {name}, {team}  ({assists} assists, {shots_on}/{shots_total} SOG)",
                    )
                )
                if i > 9:
                    break
        return top_scorers
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching golden boot leaders: {e.response.content}")
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching golden boot leaders: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching golden boot leaders: {e}")
