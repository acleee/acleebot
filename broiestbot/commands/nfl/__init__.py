import requests
from emoji import emojize
from requests.exceptions import HTTPError

from config import NFL_GAMES_URL, NFL_HTTP_HEADERS
from logger import LOGGER


def get_live_nfl_games() -> str:
    """Get summary of all live NFL games, scores and odds.

    :returns: str
    """
    try:
        params = {"status": "in progress", "league": "NFL"}
        resp = requests.get(NFL_GAMES_URL, headers=NFL_HTTP_HEADERS, params=params)
        games = resp.json().get("results")
        if resp.status_code == 429:
            return emojize(
                f":warning: yall used the command too much now they tryna charge me smh :warning:"
            )
        if games:
            game_summaries = "\n\n\n\n"
            for i, game in enumerate(games):
                summary = f"{game['teams']['away']['team']} <b>({game['scoreboard']['score']['away']})</b> @ {game['teams']['home']['team']} <b>({game['scoreboard']['score']['home']})</b>\n"
                summary += f"Period {game['scoreboard']['currentPeriod']}, {game['scoreboard']['periodTimeRemaining']}\n"
                summary += f"Spread {game['odds'][0]['spread']['open']['home']} {game['teams']['home']['abbreviation']}, {game['odds'][0]['spread']['open']['away']} {game['teams']['away']['abbreviation']}\n\n"
                game_summaries += summary
            return game_summaries
        return emojize(":warning: No live NFL games atm :( :warning:", use_aliases=True)
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching live NFL games: {e.response.content}")
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching live NFL games: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching live NFL games: {e}")
