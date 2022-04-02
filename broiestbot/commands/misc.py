"""Miscellaneous utility/novelty commands."""
from calendar import day_name
from datetime import datetime, timedelta
from typing import Optional

import requests
from emoji import emojize

from clients import sms
from config import (
    CHATANGO_SPECIAL_USERS,
    RAPID_API_KEY,
    TIMEZONE_US_EASTERN,
    TWILIO_RECIPIENT_PHONE,
    TWILIO_SENDER_PHONE,
)
from logger import LOGGER


def blaze_time_remaining() -> str:
    """
    Calculate remaining time until everybody's favorite time (EST).

    :returns: str
    """
    now = datetime.now(tz=TIMEZONE_US_EASTERN)
    am_time = now.replace(hour=4, minute=20, second=0)
    pm_time = now.replace(hour=16, minute=20, second=0)
    if am_time <= now < am_time + timedelta(seconds=59) or pm_time <= now < pm_time + timedelta(
        seconds=59
    ):
        return emojize(
            f":herb: :fire: HOLY FUCK IT'S EXACTLY 420!!! BLAZE IT BITCHHHHHHHCAWWHHHHHH :smoking: :kissing_closed_eyes: :dash:",
            language="en",
        )
    elif am_time > now:
        remaining = f"{am_time - now}"
    elif am_time < now < pm_time:
        remaining = f"{pm_time - now}"
    else:
        tomorrow_am_time = now.replace(hour=4, minute=20, second=0) + timedelta(days=1)
        remaining = f"{tomorrow_am_time - now}"
    remaining = remaining.split(":")
    return emojize(
        f":herb: :fire: \
            {remaining[0]} hours, {remaining[1]} minutes, & {remaining[2]} seconds until 4:20 \
            :smoking: :kissing_closed_eyes: :dash:",
        language="en",
    )


def send_text_message(message: str, user: str) -> Optional[str]:
    """
    Send SMS to Bro via Twilio.

    :param str message: Text message body to send via SMS.
    :param str user: Username of user attempting to send SMS.

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
            language="en",
        )
    except Exception as e:
        LOGGER.error(f"Unexpected error when sending SMS: {e}")


def time_until_wayne() -> str:
    """
    Determine amount of time remaining until LMAD.
    Only applicable to weekdays before 10am EST.

    :returns: str
    """
    try:
        now = datetime.now(tz=TIMEZONE_US_EASTERN)
        weekday = datetime.today().weekday()
        if weekday < 6:
            wayne_start_time = datetime(
                day=now.day,
                hour=10,
                minute=0,
                second=0,
                year=now.year,
                month=now.month,
                tzinfo=TIMEZONE_US_EASTERN,
            )
            wayne_end_time = wayne_start_time + timedelta(hours=1)
            if wayne_start_time < now < wayne_end_time:
                return emojize(
                    f":red_exclamation_mark: :dollar: omfg Wayne is on NOW!!! CHANGE THE CHANNOL!!! :dollar: :red_exclamation_mark:",
                    language="en",
                )
            elif wayne_end_time < now:
                return emojize(
                    f":( Wayne is oughver already today :(",
                    language="en",
                )
            else:
                time_remaining = wayne_start_time - now
                minutes_remaining = round(time_remaining.total_seconds() / 60)
                return emojize(
                    f":raising_hands_dark_skin_tone: :money_bag:  {minutes_remaining} minutes left until WAYNE :money_bag: :raising_hands_dark_skin_tone:",
                    language="en",
                )
        return emojize(
            f":warning: bruh it's {day_name[weekday]} there's no wayne today :warning:",
            language="en",
        )
    except Exception as e:
        LOGGER.error(f"Unexpected error while determining time until wayne: {e}")
        return ":warning: idk wtf you did but your lack of wayne knowledge broke bot :warning:"


def covid_cases_usa() -> str:
    """
    Retrieve reported COVID-19 cases and deaths in the US.

    :returns: str
    """
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
    covid_summary = f"\n\n\n:flag_for_United_States::eagle: USA! USA! USA! USA! :eagle::flag_for_United_States:\n:chart_increasing: {cases:,} cases\n:skull: {deaths:,} deaths\n:face_with_medical_mask: {critical:,} critical"
    return emojize(
        covid_summary,
        language="en",
    )
