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
    logger.remove()
    logger.add(sys.stderr,
               colorize=True,
               format="<light-cyan>{time:MM-DD-YYYY HH:mm:ss}</light-cyan> | "
                      + "<light-green>{level}</light-green>: "
                      + "<light-white>{message}</light-white>",
               catch=True)
    handler = NotificationHandler("gmail", defaults=params)
    logger.add(handler, level="ERROR")
    return logger
