from redis.exceptions import RedisError

from clients import r
from logger import LOGGER


def tovala_counter(value: str):
    """Keep track of consecutive Tovalas."""
    try:
        LOGGER.info(f"Saving value to redis: {value}")
        r.set("test", value)
    except RedisError as e:
        LOGGER.error(f"RedisError while saving Redis value: {e}")
