"""Parse live MLB game summary."""
from typing import Optional

from logger import LOGGER


def parse_live_mlb_game(game: dict) -> Optional[str]:
    """
    Inning-by-inning score breakdown of live Phillies game.

    :param dict game: Dictionary response of a live game summary.

    :returns: Optional[str]
    """
    try:
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
            "--------\n"
            f"<b>R</b>: {away_score} {home_score}\n"
            f"<b>H</b>: {away_hits} {home_hits}\n"
            f"<b>E</b>: {away_errors} {home_errors}"
        )
        return game_summary
    except ValueError as e:
        LOGGER.error(f"ValueError while parsing live Phillies game: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error while parsing live Phillies game: {e}")
