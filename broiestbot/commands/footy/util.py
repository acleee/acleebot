from datetime import datetime, timedelta, tzinfo
from typing import Tuple, Union

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


def get_current_day(room: str) -> datetime:
    """
    Get current date depending on Chatango room.

    :param room: Chatango room in which command was triggered.

    :returns: datetime
    """
    if room == CHATANGO_OBI_ROOM:
        return datetime.now(tz=pytz.timezone("Europe/London"))
    return datetime.now(pytz.timezone("America/New_York"))


def abbreviate_team_name(team_name: str) -> str:
    """
    Abbreviate long team names to make schedules readable.

    :param str team_name: Full team name.

    :returns: str
    """
    return (
        team_name.replace("New England", "NE")
        .replace("New York City", "NYC")
        .replace("New York", "NY")
        .replace("Paris Saint Germain", "PSG")
        .replace("Manchester United", "ManU")
        .replace("Manchester City", "Man City")
        .replace("Liverpool", "LFC")
        .replace("Philadelphia", "PHI")
        .replace("Borussia Dortmund", "Dortmund")
    )


def check_fixture_start_date(
    fixture_start_date: datetime, tz: tzinfo, display_date: str
) -> Union[str, datetime]:
    """
    Simplify fixture date if fixture occurs `Today` or `Tomorrow`.'

    :param datetime fixture_start_date: Datetime of fixture start time.
    :param tzinfo tz: Timezone of fixture start time.
    :param str display_date: Fallback string of fixture start time.

    :returns: Union[str, datetime]
    """
    if fixture_start_date.date() == datetime.date(datetime.now(tz)):
        return f"Today, {display_date.split(', ')[1]}"
    elif fixture_start_date.date() == datetime.date(datetime.now(tz)) + timedelta(
        days=1
    ):
        return f"Tomorrow, {display_date.split(', ')[1]}"
    return display_date
