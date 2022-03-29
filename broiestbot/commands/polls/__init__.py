"""Utilize Redis cache for recoding consecutive Tovalas."""
from datetime import datetime

from redis.exceptions import RedisError

from config import TIMEZONE_US_EASTERN
from clients import r
from logger import LOGGER


def tovala_counter(user_name: str) -> str:
    """
    Keep track of consecutive Tovalas.

    :param str user_name: Name of user reporting a Tovala sighting.

    :returns: str
    """
    try:
        now_string = datetime.now(tz=TIMEZONE_US_EASTERN).strftime("%Y-%m-%dT%I:%M")
        r.lpush(now_string, user_name)
        r.expire(now_string, 60)
        tovala_users = r.lrange(now_string, 0, -1)
        number_tovalas = r.llen(now_string)
        LOGGER.success(f"Saved Tovala sighting to Redis: ({now_string}, {user_name})")
        return f"{number_tovalas} CONSECUTIVE TOVALAS! Reported by: {', '.join(tovala_users)}"
    except RedisError as e:
        LOGGER.error(f"RedisError while saving Tovala streak ({now_string}, {user_name}): {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error while saving Tovala streak ({now_string}, {user_name}): {e}")
