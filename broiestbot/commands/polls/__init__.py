"""Utilize Redis cache for recoding consecutive Tovalas."""
from datetime import datetime

import pytz
from redis.exceptions import RedisError

from clients import r
from logger import LOGGER


def tovala_counter(user_name: str):
    """
    Keep track of consecutive Tovalas.

    :param str user_name: Name of user reporting a Tovala sighting.

    :returns: str
    """
    try:
        tz = pytz.timezone("US/Eastern")
        now_string = datetime.now(tz=tz).strftime("%Y-%m-%dT%I:%M")
        r.lpush(now_string, user_name)
        r.expire(now_string, 90)
        tovala_users = r.lrange(now_string, 0, -1)
        number_tovalas = r.llen(now_string)
        LOGGER.success(f"Saved {number_tovalas} values to Redis: {now_string}: {tovala_users}")
        return f"{number_tovalas} CONSECUTIVE TOVALAS! Reported by: {', '.join(tovala_users)}"
    except RedisError as e:
        LOGGER.error(f"RedisError while saving Redis value: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error while saving Redis value: {e}")
