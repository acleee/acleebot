"""Conduct a chat poll whether to 'change or stay'."""
from datetime import datetime, timedelta

from emoji import emojize
from redis.exceptions import RedisError

from clients import r
from logger import LOGGER


def change_or_stay_vote(user_name: str, vote: str) -> str:
    """
    Conduct chat-wide vote whether to 'change or stay'.
    Each user may cast a single vote, with the results revealed after a fixed time period.

    :param str user_name: Name of user submitting a vote.
    :param str vote: User's submitted vote (either 'change' or 'stay').

    :returns: str
    """
    try:
        change_votes = r.smembers("change")
        stay_votes = r.smembers("stay")
        if len(change_votes) == 0 or len(stay_votes) == 0:
            r.sadd("change", "")
            r.sadd("stay", "")
            r.sadd(vote, user_name)
            r.expire("change", 60)
            r.expire("stay", 60)
            # r.enqueue(datetime.now() + timedelta(seconds=59), poll_results)
            return emojize(
                f"\n\n"
                f":television: <b>CHANGE OR STAY!</b>\n"
                f"@{user_name} just started a poll and voted to <b>{vote}</b>.\n"
                f"Voting ends in 60 seconds.",
            )
        elif r.sismember("change", user_name) or r.sismember("stay", user_name):
            return f":warning: pls @{user_name} u already voted :warning:"
        r.lpush(vote, user_name)
        return emojize(
            f"\n\n"
            f"<b>CHANGE:</b> {change_votes}\n"
            f"<b>STAY:</b> {stay_votes}\n"
            f":alarm_clock: REMAINING: {r.ttl(vote)}",
        )
    except RedisError as e:
        LOGGER.error(f"RedisError while saving 'change or stay' vote from @{user_name}: {e}")
        return emojize(
            f":warning: my b @{user_name}, broughbert is strugglin with polls atm :warning:",
        )
    except Exception as e:
        LOGGER.error(f"Unexpected error while saving 'change or stay' vote from @{user_name}: {e}")
        return emojize(
            f":warning: my b @{user_name}, broughbert just broke like a littol BITCH :warning:",
        )


def poll_results():
    """
    Post `change or stay` poll results.

    :returns: str
    """
    change_votes = r.smembers("change")
    stay_votes = r.smembers("stay")
    if len(change_votes) > len(stay_votes):
        return f"<b>CHANGE OR STAY</b>\n" f"Chat has voted to CHANGE!"
    if len(change_votes) < len(stay_votes):
        return f"<b>CHANGE OR STAY</b>\n" f"Chat has voted to STAY!"
    return f"<b>CHANGE OR STAY</b>\n" f"Chat is in a stalemate! AAAAAA"
