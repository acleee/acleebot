"""Activate bot Night Mode"""
from datetime import datetime, timezone, timedelta
from broiestbot.services.logging import logger


def is_after_dark():
    """
    Determine if current time is in threshold for `Night Mode`.
    :return: Bool
    """
    after_dark = False
    tz = timezone(timedelta(hours=-4), name="EDT")
    now = datetime.now(tz=tz)
    start_time = datetime(year=now.year, month=now.month, day=now.day, hour=23, tzinfo=tz)
    end_time = datetime(year=now.year, month=now.month, day=now.day + 1, hour=5, tzinfo=tz)
    if start_time < now < end_time:
        after_dark = True
    return after_dark
