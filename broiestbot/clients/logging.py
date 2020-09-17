"""Create logger to catch errors, SMS on failure, and trace via Datadog."""
import sys
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
    subset = {"time": record["time"].strftime("%m/%d/%Y, %H:%M:%S"), "message": record["message"]}
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
        logger.add(
            'logs/info.log',
            colorize=True,
            format="<light-cyan>{time:MM-DD-YYYY HH:mm:ss}</light-cyan>"
            + " | <light-red>{level}</light-red>:"
            + " <light-white>{message}</light-white>",
            catch=True,
            rotation="500 MB",
            level="INFO"
        )
        logger.add(
            'logs/errors.log',
            colorize=True,
            format="<light-cyan>{time:MM-DD-YYYY HH:mm:ss}</light-cyan>"
            + " | <light-red>{level}</light-red>: "
            + " <light-white>{message}</light-white>",
            catch=True,
            rotation="500 MB",
            level="ERROR",
        )
        # Datadog
        logger.add(
            'logs/brobot.json',
            format=formatter,
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
    return logger
