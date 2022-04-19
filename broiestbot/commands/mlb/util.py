from typing import Optional

from logger import LOGGER

from .live import parse_live_mlb_game
from .upcoming import parse_upcoming_mlb_game


def parse_mlb_game(game: dict) -> Optional[str]:
    """
    Parse MLB gae response depending on game's status.

    :param dict game: Dictionary response of Phillies game.

    :returns: Optional[str]
    """
    try:
        status = game["status"]["long"]
        if status in ("Postponed", "Canceled"):
            return None
        elif status == "Not Started":
            return parse_upcoming_mlb_game(game)
        elif "Inning" in status:
            return parse_live_mlb_game(game)
    except Exception as e:
        LOGGER.error(f"Unexpected error while parsing MLB games: {e}")
