"""Create logger to catch and notify on failure."""
import sys
from notifiers.logging import NotificationHandler
from loguru import logger
from config import (TWILIO_ACCOUNT_SID,
                    TWILIO_AUTH_TOKEN,
                    TWILIO_RECIPIENT_PHONE,
                    TWILIO_SENDER_PHONE)


def create_logger():
    """Customer logger creation."""
    params = {
        'from': TWILIO_SENDER_PHONE,
        'to': TWILIO_RECIPIENT_PHONE,
        'account_sid': TWILIO_ACCOUNT_SID,
        'auth_token': TWILIO_AUTH_TOKEN,
    }
    handler = NotificationHandler("twilio", defaults=params)
    logger.remove()
    logger.add(sys.stdout,
               colorize=True,
               format="<light-cyan>{time:MM-DD-YYYY HH:mm:ss}</light-cyan> | "
               + "<light-green>{level}</light-green>: "
               + "<light-white>{message}</light-white>",
               level="INFO")
    logger.add('logs/info.log',
               colorize=True,
               format="<light-cyan>{time:MM-DD-YYYY HH:mm:ss}</light-cyan> | "
               + "<light-red>{level}</light-red>: "
               + "<light-white>{message}</light-white>",
               catch=True,
               rotation="500 MB",
               level="INFO")
    logger.add('logs/errors.log',
               colorize=True,
               format="<light-cyan>{time:MM-DD-YYYY HH:mm:ss}</light-cyan> | "
               + "<light-red>{level}</light-red>: "
               + "<light-white>{message}</light-white>",
               catch=True,
               rotation="500 MB",
               level="ERROR")
    logger.add(handler,
               catch=True,
               format="<light-red>BROBOT ERROR</light-red>: "
               + "<light-white>{message}</light-white>",
               level="ERROR")
    return logger
