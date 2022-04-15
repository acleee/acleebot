"""Fetch scheduled MLB games."""
from datetime import datetime

import pytz
import requests
from emoji import emojize
from requests.exceptions import HTTPError

from config import MLB_BASE_ENDPOINT, MLB_LEAGUE_ID, MLB_PHILLIES_ID, RAPID_API_KEY
from logger import LOGGER


def today_phillies_games() -> str:
    """
    Fetch live or upcoming Phillies games for the current date.

    :returns: str
    """
    todays_games_response = "\n\n\n\n"
    todays_games = get_todays_games()
    if bool(todays_games):
        for game in todays_games:
            todays_games_response += parse_mlb_game(game)
            return todays_games_response
    return emojize(":warning: Couldn't find any MLB games :( :warning:", use_aliases=True)


def get_todays_games():
    try:
        url = f"{MLB_BASE_ENDPOINT}/games"
        today = datetime.now(pytz.timezone("America/New_York")).strftime("%Y-%m-%d")
        params = {"league": MLB_LEAGUE_ID, "season": "2022", "team": MLB_PHILLIES_ID, "date": today}
        headers = {
            "X-RapidAPI-Host": "api-baseball.p.rapidapi.com",
            "X-RapidAPI-Key": RAPID_API_KEY,
        }
        resp = requests.get(url, headers=headers, params=params)
        if resp.status_code == 200 and resp.json():
            return resp.json().get("response")
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching MLB games: {e.response.content}")
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching MLB games: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching MLB games: {e}")


def parse_mlb_game(game: dict):
    try:
        status = game["status"]["long"]
        if status in ("Postponed", "Canceled"):
            return None
        elif status == "Not Started":
            return upcoming_mlb_game(game)
        elif "Inning" in status:
            return live_mlb_game(game)
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching MLB games: {e}")


def upcoming_mlb_game(game: dict):
    home_name = game["teams"]["home"]
    away_name = game["teams"]["away"]
    start_time = game["time"]
    return f"<b>{away_name}</b> @ <b>{home_name}</b>\n{start_time}"


def live_mlb_game(game: dict):
    home_name = game["teams"]["home"]["name"].split(" ")[-1]
    home_abbreviation = home_name[0:3].upper()
    home_score = game["scores"]["home"]["total"]
    home_hits = game["scores"]["home"]["hits"]
    home_errors = game["scores"]["home"]["errors"]
    away_name = game["teams"]["away"]["name"].split(" ")[-1]
    away_abbreviation = away_name[0:3].upper()
    away_score = game["scores"]["away"]["total"]
    away_hits = game["scores"]["away"]["hits"]
    away_errors = game["scores"]["away"]["errors"]
    home_innings = game["scores"]["home"]["innings"]
    away_innings = game["scores"]["away"]["innings"]
    game_summary = (
        f"{away_abbreviation} <b>{away_score}</b> @ {home_abbreviation} <b>{home_score}</b>\n"
    )
    for k, v in away_innings.items():
        if v is not None:
            game_summary += f"<b>{k}</b>:   {away_innings[k]}   {home_innings[k]}\n"
    game_summary += (
        "\n"
        f"<b>{away_name}</b>: {away_hits} hits, {away_errors} errors\n"
        f"<b>{home_name}</b>: {home_hits} hits, {home_errors} errors"
    )
    return game_summary
