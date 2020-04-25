import sys
from notifiers.logging import NotificationHandler
from loguru import logger
from config import GMAIL_EMAIL, GMAIL_PASSWORD


def notification_logger():
    params = {
        "username": GMAIL_EMAIL,
        "password": GMAIL_PASSWORD,
        "to": GMAIL_EMAIL
    }
    logger.add(sys.stderr,
               colorize=True,
               format="<green>{time:MM-DD HH:mm A}</green> <white>{message}</white>",
               catch=True)
    handler = NotificationHandler("gmail", defaults=params)
    logger.add(handler, level="ERROR")
    return logger
