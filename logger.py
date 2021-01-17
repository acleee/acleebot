"""Custom logger and error notifications."""
import re
from sys import stdout

import simplejson as json
from loguru import logger

from clients import sms
from config import ENVIRONMENT, TWILIO_RECIPIENT_PHONE, TWILIO_SENDER_PHONE


def formatter(record):
    """Format info message logs."""

    def serialize_as_admin(log):
        """Construct JSON info log record."""
        chat_data = re.findall(r"\[(\S+)\]", log["message"])
        if bool(chat_data):
            room = chat_data[0]
            user = chat_data[1]
            ip = chat_data[2]
            subset = {
                "time": log["time"].strftime("%m/%d/%Y, %H:%M:%S"),
                "message": log["message"].split(": ", 1)[1],
                "level": log["level"].name,
                "room": room,
                "user": user,
                "ip": ip,
            }
            return json.dumps(subset)

    def serialize_event(log):
        """Construct JSON warning log record."""
        chat_data = re.findall(r"\[(\S+)\]", log["message"])
        if bool(chat_data):
            room = chat_data[0]
            user = chat_data[1]
            subset = {
                "time": log["time"].strftime("%m/%d/%Y, %H:%M:%S"),
                "message": log["message"].split(": ", 1)[1],
                "level": log["level"].name,
                "room": room,
                "user": user,
            }
            return json.dumps(subset)

    def serialize_error(log):
        """Construct JSON error log record."""
        subset = {
            "time": log["time"].strftime("%m/%d/%Y, %H:%M:%S"),
            "level": log["level"].name,
            "message": log["message"],
        }
        return json.dumps(subset)

    if record["level"].name in ("WARNING", "SUCCESS"):
        record["extra"]["serialized"] = serialize_event(record)
        return "{extra[serialized]},\n"

    elif record["level"].name == "INFO":
        record["extra"]["serialized"] = serialize_as_admin(record)
        return "{extra[serialized]},\n"

    else:
        record["extra"]["serialized"] = serialize_error(record)
        error_handler(record)
        return "{extra[serialized]},\n"


def error_handler(record):
    sms.messages.create(
        body=f'BROBOT ERROR: {record["time"].strftime("%m/%d/%Y, %H:%M:%S")} | {record["message"]}',
        from_=TWILIO_SENDER_PHONE,
        to=TWILIO_RECIPIENT_PHONE,
    )


def create_logger() -> logger:
    """Customer logger creation."""
    logger.remove()
    logger.add(
        stdout,
        colorize=True,
        catch=True,
        format="<light-cyan>{time:MM-DD-YYYY HH:mm:ss}</light-cyan> | "
        + "<light-green>{level}</light-green>: "
        + "<light-white>{message}</light-white>",
    )
    if ENVIRONMENT == "production":
        logger.add(
            "/var/log/broiestbot/info.json",
            format=formatter,
            rotation="200 MB",
            compression="zip",
            catch=True,
        )
        logger.add(
            "/var/log/broiestbot/info.log",
            colorize=True,
            catch=True,
            format="<light-cyan>{time:MM-DD-YYYY HH:mm:ss}</light-cyan> | "
            + "<light-green>{level}</light-green>: "
            + "<light-white>{message}</light-white>",
            rotation="500 MB",
            compression="zip",
        )
    return logger


LOGGER = create_logger()
