"""Create logger to catch errors, SMS on failure, and trace via Datadog."""
import sys
import re
import simplejson as json
from loguru import logger
from notifiers.logging import NotificationHandler
from config import (
    ENVIRONMENT,
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_RECIPIENT_PHONE,
    TWILIO_SENDER_PHONE
)


def serialize(record):
    """Construct JSON log record."""
    room = re.findall(r'\[(\S+)\]', record["message"])[0]
    user = re.findall(r'\[(\S+)\]', record["message"])[1]
    ip = re.findall(r'\[(\S+)\]', record["message"])[2]
    subset = {
        "time": record["time"].strftime("%m/%d/%Y, %H:%M:%S"),
        "message": record["message"].split(': ', 1)[1],
        "room": room,
        "user": user,
        "ip": ip
    }
    return json.dumps(subset)


def formatter(record):
    record["extra"]["serialized"] = serialize(record)
    return "{extra[serialized]},\n"


def create_logger():
    """Customer logger creation."""
    logger.remove()
    if ENVIRONMENT == 'production':
        params = {
            'from': TWILIO_SENDER_PHONE,
            'to': TWILIO_RECIPIENT_PHONE,
            'account_sid': TWILIO_ACCOUNT_SID,
            'auth_token': TWILIO_AUTH_TOKEN,
        }
        handler = NotificationHandler("twilio", defaults=params)
        # Datadog
        logger.add(
            'logs/brobot.json',
            format=formatter,
            level="INFO"
        )
        logger.add(
            'logs/errors.json',
            format=formatter,
            level="ERROR"
        )
        # SMS
        logger.add(
            handler,
            catch=True,
            level="ERROR"
        )
    else:
        logger.add(
            sys.stdout,
            colorize=True,
            format="<light-cyan>{time:MM-DD-YYYY HH:mm:ss}</light-cyan>"
                   + " | <light-green>{level}</light-green>: "
                   + " <light-white>{message}</light-white>",
            level="INFO"
        )
        logger.add(
            sys.stderr,
            colorize=True,
            format="<light-cyan>{time:MM-DD-YYYY HH:mm:ss}</light-cyan>"
                   + " | <light-red>{level}</light-red>: "
                   + " <light-white>{message}</light-white>",
            catch=True,
            level="ERROR"
        )
        logger.add(
            sys.stdout,
            format=formatter,
        )
    return logger


LOGGER = create_logger()
