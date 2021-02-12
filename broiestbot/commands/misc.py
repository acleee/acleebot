"""Miscellaneous utility/novelty commands."""
from datetime import datetime, timedelta
from typing import Optional

import pytz
import requests
from emoji import emojize

from clients import sms
from config import (
    CHATANGO_SPECIAL_USERS,
    RAPID_API_KEY,
    TWILIO_RECIPIENT_PHONE,
    TWILIO_SENDER_PHONE,
)
from logger import LOGGER


def blaze_time_remaining() -> str:
    """
    Calculate remaining time until everybody's favorite time (EST).

    :returns: str
    """
    now = datetime.now(tz=pytz.timezone("America/New_York"))
    am_time = now.replace(hour=4, minute=20, second=0)
    pm_time = now.replace(hour=16, minute=20, second=0)
    if am_time > now:
        remaining = f"{am_time - now}"
    elif am_time < now < pm_time:
        remaining = f"{pm_time - now}"
    else:
        tomorrow_am_time = now.replace(day=now.day + 1, hour=4, minute=20, second=0)
        remaining = f"{tomorrow_am_time - now}"
    remaining = remaining.split(":")
    return emojize(
        f":herb: :fire: \
            {remaining[0]} hours, {remaining[1]} minutes, & {remaining[2]} seconds until 4:20 \
            :smoking: :kissing_closed_eyes: :dash:",
        use_aliases=True,
    )


def send_text_message(message: str, user: str) -> Optional[str]:
    """
    Send SMS to Bro via Twilio.

    :param message: Text message body to send via SMS.
    :type message: str
    :param user: User attempting to send SMS.
    :type user: str
    :returns: Optional[str]
    """
    try:
        if user.lower() in CHATANGO_SPECIAL_USERS:
            sms.messages.create(
                body=f"{user.upper()}: {message}",
                from_=TWILIO_SENDER_PHONE,
                to=TWILIO_RECIPIENT_PHONE,
            )
            return f"ty @{user} I just texted brough: {message}"
        return emojize(
            f":warning: lmao fuck off, only pizza can text brough :warning:",
            use_aliases=True,
        )
    except Exception as e:
        LOGGER.error(f"Unexpected error when sending SMS: {e}")


def covid_cases_usa():
    covid_by_state = "\n\n\n"
    url = "https://covid-19-data.p.rapidapi.com/country/code"
    params = {
        "code": "usa",
        "format": "json",
    }
    headers = {
        "x-rapidapi-key": RAPID_API_KEY,
        "x-rapidapi-host": "covid-19-data.p.rapidapi.com",
    }
    res = requests.get(url, headers=headers, params=params).json()[0]
    deaths = res["deaths"]
    critical = res["critical"]
    cases = res["confirmed"]
    covid_summary = f"\n\n:flag_for_United_States::eagle: USA! USA! USA! USA! :eagle::flag_for_United_States:\n:chart_increasing: {cases:,} cases\n:skull: {deaths:,} deaths\n:face_with_medical_mask: {critical:,} critical"
    return emojize(
        covid_summary,
        use_aliases=True,
    )
