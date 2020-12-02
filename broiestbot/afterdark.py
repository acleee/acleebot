"""Activate bot Night Mode"""
from datetime import datetime

import pytz


def is_after_dark() -> bool:
    """
    Determine if current time is in threshold for `Night Mode`.
    :return: Bool
    """
    tz = pytz.timezone("America/New_York")
    now = datetime.now(tz=pytz.timezone("America/New_York"))
    start_time = datetime(
        year=now.year, month=now.month, day=now.day, hour=0, tzinfo=tz
    )
    end_time = datetime(year=now.year, month=now.month, day=now.day, hour=5, tzinfo=tz)
    if start_time < now < end_time:
        return True
    return False
