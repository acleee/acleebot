"""Conduct a chat poll whether to 'change or stay'."""
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
        if r.sismember("change", user_name) or r.sismember("stay", user_name):
            return emojize(f":warning: <b>pls @{user_name} u already voted</b> :warning:", lang="en")
        r.sadd(vote, user_name)
        if change_votes is None:
            r.sadd("change", "")
            r.expire("change", 60)
        elif stay_votes is None:
            r.sadd("stay", "")
            r.expire("stay", 60)
        # if not votes_to_change or not votes_to_stay:
        #    r.sadd("change", "")
        #    r.sadd("stay", "")
        #    r.sadd(vote, user_name)
        # r.enqueue(datetime.now() + timedelta(seconds=60), poll_results)
        return poll_announcement(user_name, vote)
    except RedisError as e:
        LOGGER.error(f"RedisError while saving 'change or stay' vote from @{user_name}: {e}")
        return emojize(
            f":warning: my b @{user_name}, broughbert is strugglin with polls atm :warning:",
            language="en",
        )
    except Exception as e:
        LOGGER.error(f"Unexpected error while saving 'change or stay' vote from @{user_name}: {e}")
        return emojize(
            f":warning: my b @{user_name}, broughbert just broke like a littol BITCH :warning:",
            language="en",
        )


def initialize_poll(user_name: str) -> str:
    """
    Initialize a poll (if exists) or summarize the status of a preexisting poll.

    :param str user_name: Name of user submitting a vote.
    :param str vote: User's submitted vote (either 'change' or 'stay').

    :returns: str
    """
    change_votes = r.smembers("change")
    stay_votes = r.smembers("stay")
    return emojize(
        f"\n\n"
        f":television: <b>CHANGE OR STAY!</b>\n"
        f"@{user_name} just started a poll.\n"
        f":hourglass_not_done: Voting ends in <i>60 seconds</i>.\n"
        f"\n"
        f":shuffle_tracks_button: !CHANGE: <b>{len(change_votes)}</b> votes\n"
        f":stop_button: !STAY <b>{len(stay_votes)}</b> votes\n\n",
        language="en",
    )


def poll_announcement(user_name: str, vote: str) -> str:
    """
    Summarize the status of a preexisting poll.

    :param str user_name: Name of user submitting a vote.
    :param str vote: User's submitted vote (either 'change' or 'stay').

    :returns: str
    """
    return emojize(
        f"\n\n"
        f":television: <b>CHANGE OR STAY!</b>\n"
        f"@{user_name} just started a poll and voted to <b>{vote}</b>.\n"
        f"Voting ends in 60 seconds.",
        language="en",
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
