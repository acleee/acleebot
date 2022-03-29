from typing import Dict

import pytest
from redis import Redis

from config import REDIS_DB, REDIS_HOST, REDIS_PASSWORD, REDIS_PORT


@pytest.fixture
def redis_mock() -> Redis:
    """
    Initialize connection to Redis instance.

    :returns: Redis
    """
    return Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        db=REDIS_DB,
        decode_responses=True,
    )


@pytest.fixture
def tovala_poll_results() -> Dict[str, str]:
    """
    Example result of a collective Tovala sighting between 3 users.

    :returns: Dict[str, str]
    """
    return {
        "broiestbro": str(1),
        "broiestbot": str(1),
        "acleebot": str(1),
    }
