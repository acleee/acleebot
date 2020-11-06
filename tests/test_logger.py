from twilio.rest import Client

from config import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_RECIPIENT_PHONE,
    TWILIO_SENDER_PHONE,
)
from logger import LOGGER


def test_sms():
    sms = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    sms.messages.create(
        body="This is a test Twilio message from Broiestbot.",
        from_=TWILIO_SENDER_PHONE,
        to=TWILIO_RECIPIENT_PHONE,
    )


def test_sms_logger():
    LOGGER.error("This is a test ERROR log from Broiestbot.")
