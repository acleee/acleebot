"""Conduct a chat poll whether to 'change or stay'."""
from emoji import emojize
from redis.exceptions import RedisError

from clients import r
from logger import LOGGER


def change_or_stay_vote(user_name: str, vote: str, room_name: str) -> str:
    """
    Conduct chat-wide vote whether to 'change or stay'.
    Each user may cast a single vote, with the results revealed after a fixed time period.

    :param str user_name: Name of user submitting a vote.
    :param str vote: User's submitted vote (either 'change' or 'stay').
    :param str room_name: Chatango room in which the poll is taking place.

    :returns: str
    """
    try:
        change_votes = r.smembers("change")
        stay_votes = r.smembers("stay")
        if change_votes is None and stay_votes is None:
            r.expire("change", 60)
            r.expire("stay", 60)
            r.sadd(vote, user_name)
            return f"<b>CHANGE OR STAY!</b>\n@{user_name} just started a poll and voted to <b>{vote}</b>.\nVoting ends in 60 seconds."
        r.sadd(vote, user_name)
        return f"<b>CHANGE OR STAY:</b>\nCHANGE: {change_votes}\nSTAY: {stay_votes}\n:alarm_clock:REMAINING: {r.ttl(vote)/100}"
    except RedisError as e:
        LOGGER.error(f"RedisError while saving 'change or stay' vote from @{user_name}: {e}")
        return emojize(
            f":warning: my b @{user_name}, broughbert is strugglin with polls atm :warning:",
            use_aliases=True,
        )
    except Exception as e:
        LOGGER.error(f"Unexpected error while saving 'change or stay' vote from @{user_name}: {e}")
        return emojize(
            f":warning: my b @{user_name}, broughbert just broke like a littol BITCH :warning:",
            use_aliases=True,
        )
