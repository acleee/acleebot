"""Allow users to track consecutive Tovala streaks via Redis cache."""
from typing import Dict

from emoji import emojize
from redis import Redis

from broiestbot.commands.polls import tally_tovala_sightings_by_user, tovala_counter
from config import CHATANGO_BOTS


def test_tovala_counter(redis_mock: Redis, tovala_poll_results: Dict[str, str]):
    """
    Conduct a mock Tovala streak & ensure value are stored correctly.

    :param Redis redis_mock: Connection to Redis instance.
    :param Dict[str, str] tovala_poll_results: Example result of a collective Tovala sighting between 3 users.
    """
    flush_tovala_cache(redis_mock)
    for username in CHATANGO_BOTS:
        counter = tovala_counter(username.lower())
        assert redis_mock.hexists("tovala", username.lower()) is True
        assert redis_mock.hget("tovala", username.lower()) == str(1)
        assert formatted_tovala_result(redis_mock) == counter
    assert redis_mock.hgetall("tovala") == tovala_poll_results


def flush_tovala_cache(r: Redis):
    """
    Remove existing Tovala hash prior to running test.

    :param Redis r: Connection to Redis instance.
    """
    for username in CHATANGO_BOTS:
        r.hdel("tovala", username.lower())
    assert len(r.hgetall("tovala")) == 0


def formatted_tovala_result(r: Redis) -> str:
    """
    Format existing Tovala poll results into a text-based response.

    :param Redis r: Connection to Redis instance.

    :returns: str
    """
    number_tovalas = len(r.hvals("tovala"))
    tovala_users = r.hgetall("tovala")
    return emojize(
        f"\n\n<b>:shallow_pan_of_food: {number_tovalas} CONSECUTIVE TOVALAS!</b>\n{tally_tovala_sightings_by_user(tovala_users)}\n:keycap_#: Highest streak: 3",
        language="en",
    )
