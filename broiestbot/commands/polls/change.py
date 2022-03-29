"""Conduct a chat poll whether to 'change or stay.'"""
from emoji import emojize
from redis.exceptions import RedisError

from clients import r
from logger import LOGGER


def change_or_stay(user_name: str, vote: str, room_name: str) -> str:
    """
    Conduct chat-wide vote whether to 'change or stay'. Each user may cast a single vote, with the results revealed after a dynamic time period.

    :param str user_name: Name of user submitting a vote.
    :param str vote: User's submitted vote (either 'change' or 'stay'.
     :param str room_name: Chatango room in which the poll is taking place.

    :returns: str
    """
    try:
        return "WIP"
    except RedisError as e:
        LOGGER.error(f"RedisError while saving 'change or stay' vote from @{user_name}: {e}")
        return emojize(
            f":warning: my b @{user_name}, broughbert just broke like a littol BITCH :warning:",
            use_aliases=True,
        )
    except Exception as e:
        LOGGER.error(f"Unexpected error while saving 'change or stay' vote from @{user_name}: {e}")
        return emojize(
            f":warning: my b @{user_name}, broughbert just broke like a littol BITCH :warning:",
            use_aliases=True,
        )
