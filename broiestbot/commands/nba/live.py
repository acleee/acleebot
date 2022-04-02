"""Parse live NBA scores, or fallback to upcoming games."""
from emoji import emojize
from requests.exceptions import HTTPError

from logger import LOGGER

from .today import today_nba_games
from .upcoming import upcoming_nba_games


def live_nba_games() -> str:
    """
    Fetch all live NBA games.

    :returns: str
    """
    try:
        games = "\n\n\n"
        resp = today_nba_games()
        if resp.status_code == 200:
            live_games = [
                game
                for game in resp.json()["response"]
                if game["status"]["short"] != "NS" and game["status"]["short"] != "FT"
            ]
            if len(live_games) > 0:
                games += emojize(":basketball: <b>Live NBA Games:</b>\n", language="en")
                for game in live_games:
                    away_team = game["teams"]["away"]["name"]
                    away_team_score = game["scores"]["away"]["total"]
                    home_team = game["teams"]["home"]["name"]
                    home_team_score = game["scores"]["home"]["total"]
                    game_clock = game["status"]["timer"]
                    games += f"{away_team} <b>{away_team_score}</b> @ {home_team} <b>{home_team_score}</b>\n{game_clock}"
                return games
            elif len(resp.json()["response"]) > 0:
                upcoming_games = upcoming_nba_games()
                games += f"No live NBA games. Upcoming games today:\n"
                games += upcoming_games
                return games
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching NBA games: {e.response.content}")
    except LookupError as e:
        LOGGER.error(f"LookupError while fetching NBA games: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching NBA games: {e}")


"""def live_nba_games() -> str:
    try:
        endpoint = "https://livescore6.p.rapidapi.com/matches/v2/list-by-date"
        params = {"Category": "basketball", "Date": "20210521"}
        headers = {
            "content-type": "application/json",
            "x-rapidapi-key": RAPID_API_KEY,
            "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
        }
        req = requests.get(endpoint, headers=headers, params=params)
        if req.status_code == 200:
            data = req.json()["Stages"][0]
            if data["Cid"] != "NBA":
                return emojize(
                    f":warning:️️ idk what happened I died :warning:",
                    language='en',
                )
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching NBA games: {e.response.content}")
    except LookupError as e:
        LOGGER.error(f"LookupError while fetching NBA games: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching NBA games: {e}")"""
