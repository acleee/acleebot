"""Miscellaneous utility commands."""
from calendar import day_name
from datetime import datetime, timedelta
from typing import Optional
from math import floor

import requests
from emoji import emojize

from clients import sms
from config import (
    CHATANGO_SPECIAL_USERS,
    RAPID_API_KEY,
    TIMEZONE_US_EASTERN,
    TWILIO_PHONE_NUMBERS,
    TWILIO_SENDER_PHONE,
    HTTP_REQUEST_TIMEOUT,
    COVID_API_ENDPOINT,
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
    if am_time <= now < am_time + timedelta(seconds=59) or pm_time <= now < pm_time + timedelta(seconds=59):
        return emojize(
            f":herb: :fire: HOLY FUCK IT'S EXACTLY 420!!! BLAZE IT BITCHHHHHHHCAWWHHHHHH :cigarette: :kissing_face_with_closed_eyes: :dashing_away:",
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
            :smoking: :kissing_face_with_closed_eyes: :dashing_away:",
        language="en",
    )


def send_text_message(message: str, user: str, recipient: str) -> Optional[str]:
    """
    Send SMS to Bro via Twilio.

    :param str message: Text message body to send via SMS.
    :param str user: Username of user attempting to send SMS.
    :param str recipient: 'Recipient' of the outgoing SMS message.

    :returns: Optional[str]
    """
    try:
        if user.lower() in CHATANGO_SPECIAL_USERS:
            phone_number = TWILIO_PHONE_NUMBERS.get(recipient)
            if phone_number:
                LOGGER.warning(f"Sending SMS to {recipient} from {user}: {message}")
                sms.messages.create(
                    body=f"{user.upper()}: {message}",
                    from_=TWILIO_SENDER_PHONE,
                    to=phone_number,
                )
                LOGGER.success(f"Sent SMS to {recipient} from {user}: {message}")
                return emojize(
                    f":check_mark_button: :mobile_phone: cheers @{user} I just texted ur message to {recipient} :mobile_phone: :check_mark_button:",
                    language="en",
                )
            return emojize(f":warning: ya uhhh idk who tf that is @{user} :warning:", language="en")
        return emojize(f":warning: @{user} pls, only pizzaough can text brough :warning:", language="en")
    except Exception as e:
        LOGGER.error(f"Unexpected error when sending SMS: {e}")


def time_until_wayne(user_name: str) -> str:
    """
    Determine amount of time remaining until LMAD.
    Only applicable to weekdays before 10am EST.

    :param str user_name: Name of the user inquiring about Wayne.

    :returns: str
    """
    try:
        now = datetime.now(tz=TIMEZONE_US_EASTERN)
        weekday = datetime.today().weekday()
        if weekday < 5:
            wayne_start_time = now.replace(hour=10, minute=0, second=0)
            wayne_end_time = wayne_start_time + timedelta(hours=1)
            if wayne_start_time <= now <= wayne_end_time:
                return emojize(
                    f":red_exclamation_mark: omfg Wayne is on NOW!!! CHANGE THE CHANNOL!!! :red_exclamation_mark:",
                    language="en",
                )
            elif wayne_end_time < now:
                return emojize(f":( sry @{user_name}, Wayne is oughver already today :(", language="en")
            else:
                time_remaining = wayne_start_time - now
                minutes_remaining = round(time_remaining.total_seconds() / 60)
                hours_remaining = minutes_remaining / 60
                if hours_remaining >= 1:
                    minutes_remaining = minutes_remaining % 60
                    hours_remaining = floor(hours_remaining)
                    return emojize(
                        f":raising_hands_dark_skin_tone: :money_bag: <b>{hours_remaining}h {minutes_remaining}m</b> left until WAYNE :money_bag: :raising_hands_dark_skin_tone:",
                        language="en",
                    )
                return emojize(
                    f":raising_hands_dark_skin_tone: :money_bag: <b>{minutes_remaining} minutes</b> left until WAYNE :money_bag: :raising_hands_dark_skin_tone:",
                    language="en",
                )
        return emojize(
            f":warning: bruh it's {day_name[weekday]} there's no wayne today :warning:",
            language="en",
        )
    except Exception as e:
        LOGGER.error(f"Unexpected error while determining time until wayne: {e}")
        return emojize(
            ":warning: idk wtf you did but your lack of wayne knowledge broke bot :warning:",
            language="en",
        )


def covid_cases_usa() -> str:
    """
    Retrieve reported COVID-19 cases and deaths in the US.

    :returns: str
    """
    try:
        params = {
            "code": "usa",
            "format": "json",
        }
        headers = {
            "x-rapidapi-key": RAPID_API_KEY,
            "x-rapidapi-host": "covid-19-data.p.rapidapi.com",
        }
        resp = requests.get(COVID_API_ENDPOINT, headers=headers, params=params, timeout=HTTP_REQUEST_TIMEOUT).json()[0]
        deaths = resp["deaths"]
        critical = resp["critical"]
        cases = resp["confirmed"]
        covid_summary = (
            f"\n\n\n"
            f":United_States: :eagle: USA! USA! USA! USA! :eagle: :United_States:\n"
            f":chart_increasing: {cases:,} cases\n:skull: {deaths:,} deaths\n"
            f":face_with_medical_mask: {critical:,} critical"
        )
        return emojize(covid_summary, language="en")
    except Exception as e:
        LOGGER.error(f"Unexpected error while retrieving COVID-19 data: {e}")
        return emojize(f":warning: Unexpected error while retrieving COVID-19 data: {e}", language="en")
