from datetime import datetime
from typing import Tuple

import pytz
from pytz import BaseTzInfo

from config import CHATANGO_OBI_ROOM, METRIC_SYSTEM_USERS


def get_preferred_timezone(room: str, username: str) -> dict:
    """
    Display fixture dates depending on preferred timezone of requesting user.

    :param str room: Chatango room which triggered the command.
    :param str username: Chatango user who triggered the command.

    :returns: dict
    """
    if room == CHATANGO_OBI_ROOM or username in METRIC_SYSTEM_USERS:
        return {}
    return {"timezone": "America/New_York"}


def get_preferred_time_format(
    start_time: datetime, room: str, username: str
) -> Tuple[str, BaseTzInfo]:
    """
    Display fixture times depending on preferred timezone of requesting user/room.

    :param datetime start_time: Fixture start time/date defaulted to UTC time.
    :param str room: Chatango room in which command was triggered.
    :param str username: Name of user who triggered the command.

    :returns: Tuple[str, BaseTzInfo]
    """
    if room == CHATANGO_OBI_ROOM or username in METRIC_SYSTEM_USERS:
        return start_time.strftime("%b %d, %H:%M"), pytz.utc
    return (
        start_time.strftime("%b %d, %l:%M%p").replace("AM", "am").replace("PM", "pm"),
        pytz.timezone("America/New_York"),
    )