"""Allow users to track consecutive Tovala streaks via Redis cache."""
from emoji import emojize
from redis.exceptions import RedisError

from clients import r
from logger import LOGGER


def tovala_counter(user_name: str) -> str:
    """
    Keep track of consecutive Tovalas.

    :param str user_name: Name of user reporting a Tovala sighting.

    :returns: str
    """
    try:
        r.hincrby("tovala", user_name, 1)
        r.expire("tovala", 60)
        tovala_users = r.hkeys("tovala")
        number_tovalas = r.hlen("tovala")
        LOGGER.success(f"Saved Tovala sighting to Redis: (tovala, {user_name})")
        return emojize(
            f"\n\n<b>:shallow_pan_of_food: {number_tovalas} CONSECUTIVE TOVALAS!</b>\n:bust_in_silhouette: Contributors: {', '.join(tovala_users)}\n:keycap_#: Highest streak: 3",
            use_aliases=True,
        )
    except RedisError as e:
        LOGGER.error(f"RedisError while saving Tovala streak from @{user_name}: {e}")
        return emojize(
            f":warning: my b @{user_name}, broughbert just broke like a littol BITCH :warning:",
            use_aliases=True,
        )
    except Exception as e:
        LOGGER.error(f"Unexpected error while saving Tovala streak from @{user_name}: {e}")
        return emojize(
            f":warning: my b @{user_name}, broughbert just broke like a littol BITCH :warning:",
            use_aliases=True,
        )
