"""Miscellaneous utility/novelty commands."""
from datetime import datetime
from typing import Optional

import pytz
from emoji import emojize

from clients import sms
from config import CHATANGO_SPECIAL_USERS, TWILIO_RECIPIENT_PHONE, TWILIO_SENDER_PHONE
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
