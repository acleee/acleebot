"""Custom logger and notifications."""
from sys import stdout
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


def formatter(record):
    """Format info message logs."""

    def serialize_info(log):
        """Construct JSON info log record."""
        chat_data = re.findall(r'\[(\S+)\]', log["message"])
        if bool(chat_data):
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

    def serialize_warning(log):
        """Construct JSON warning log record."""
        chat_data = re.findall(r'\[(\S+)\]', log["message"])
        if bool(chat_data):
            room = chat_data[0]
            user = chat_data[1]
            subset = {
                "time": record["time"].strftime("%m/%d/%Y, %H:%M:%S"),
                "message": record["message"].split(': ', 1)[1],
                "room": room,
                "user": user,
            }
            return json.dumps(subset)

    def serialize_error(log):
        """Construct JSON error log record."""
        subset = {
            "time": log["time"].strftime("%m/%d/%Y, %H:%M:%S"),
            "message": log["message"],
        }
        return json.dumps(subset)

    if record["level"].name == "WARNING":
        record["extra"]["serialized"] = serialize_warning(record)
        return "{extra[serialized]},\n"

    elif record["level"].name == "INFO":
        record["extra"]["serialized"] = serialize_info(record)
        return "{extra[serialized]},\n"

    else:
        record["extra"]["serialized"] = serialize_error(record)
        return "{extra[serialized]},\n"


def create_logger():
    """Customer logger creation."""
    logger.remove()
    logger.add(
        stdout,
        format=formatter,
    )
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
            format=formatter,
            rotation="500 MB",
            compression="zip"
        )
        # SMS
        logger.add(
            handler,
            catch=True,
            level="ERROR"
        )

    return logger


LOGGER = create_logger()
