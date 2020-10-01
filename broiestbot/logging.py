"""Custom logger and notifications."""
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


def serialize_info(record):
    """Construct JSON info log record."""
    chat_data = re.findall(r'\[(\S+)\]', record["message"])
    room = chat_data[0]
    user = chat_data[1]
    ip = chat_data[2]
    subset = {
        "time": record["time"].strftime("%m/%d/%Y, %H:%M:%S"),
        "message": record["message"].split(': ', 1)[1],
        "room": room,
        "user": user,
        "ip": ip
    }
    return json.dumps(subset)


def serialize_error(record):
    """Construct JSON error log record."""
    subset = {
        "time": record["time"].strftime("%m/%d/%Y, %H:%M:%S"),
        "message": record["message"],
    }
    return json.dumps(subset)


def info_formatter(record):
    """Format info message logs."""
    record["extra"]["serialized"] = serialize_info(record)
    return "{extra[serialized]},\n"


def error_formatter(record):
    """Format error message logs."""
    record["extra"]["serialized"] = serialize_error(record)
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
            'logs/info.json',
            format=info_formatter,
            level="INFO"
        )
        logger.add(
            'logs/errors.json',
            format=error_formatter,
            level="ERROR"
        )
        logger.add(
            'logs/errors.json',
            format=error_formatter,
            level="WARNING"
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
            level="WARNING"
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
    return logger


LOGGER = create_logger()
