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
        tovala_users = r.hgetall("tovala")
        tovala_contributors = tally_tovala_sightings_by_user(tovala_users)
        total_sightings = total_tovala_sightings(tovala_users)
        LOGGER.success(f"Saved Tovala sighting to Redis: (tovala, {user_name})")
        return emojize(
            f"\n\n<b>:shallow_pan_of_food: {total_sightings} CONSECUTIVE TOVALAS!</b>\n{tovala_contributors}\n:keycap_#: Highest streak: 3"
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


def tally_tovala_sightings_by_user(tovala_users: dict) -> str:
    """
    Construct summary of reported Tovala sightings by user.

    :param dict tovala_users: Map of Tovala sightings by username.

    :returns: str
    """
    contributors = ":bust_in_silhouette: Contributors: "
    for k, v in tovala_users.items():
        contributors += f"{k}: {v}, "
    return contributors.rstrip(", ")


def total_tovala_sightings(tovala_users: dict) -> int:
    """
    Aggregate sum of all Tovala sightings.

    :param dict tovala_users: Map of Tovala sightings by username.

    :returns: int
    """
    total_count = 0
    for user_count in tovala_users.values():
        total_count += int(user_count)
    return total_count
