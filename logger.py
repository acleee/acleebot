"""Custom logger and error notifications."""
import re
from sys import stdout

import simplejson as json
from loguru import logger

from clients import sms
from config import ENVIRONMENT, TWILIO_RECIPIENT_PHONE, TWILIO_SENDER_PHONE


def json_formatter(record: dict):
    """
    Format info message logs.

    :param record: Log object containing log metadata & message.
    :type record: dict
    """

    def serialize_as_admin(log: dict) -> str:
        """
        Construct JSON info log record where user is room admin.

        :param log: Dictionary containing logged message with metadata.
        :type log: dict
        :returns: str
        """
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

    def serialize_event(log: dict) -> str:
        """
        Construct warning log.

        :param log: Dictionary containing logged message with metadata.
        :type log: dict
        :returns: str
        """
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

    def serialize_error(log: dict) -> str:
        """
        Construct error log record.

        :param log: Dictionary containing logged message with metadata.
        :type log: dict
        :returns: str
        """
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


def error_handler(log: dict) -> None:
    sms.messages.create(
        body=f'BROBOT ERROR: {log["time"].strftime("%m/%d/%Y, %H:%M:%S")} | {log["message"]}',
        from_=TWILIO_SENDER_PHONE,
        to=TWILIO_RECIPIENT_PHONE,
    )


def log_formatter(record: dict) -> str:
    """
    Formatter for .log records

    :param record: Log object containing log metadata & message.
    :type record: dict
    :returns: str
    """
    if record["level"].name == "TRACE":
        return "<light-white>{time:MM-DD-YYYY HH:mm:ss}</light-white> | <fg #cfe2f3>{level}</fg #cfe2f3>: <light-white>{message}</light-white>\n"
    elif record["level"].name == "INFO":
        return "<light-white>{time:MM-DD-YYYY HH:mm:ss}</light-white> | <fg #b3cfe7>{level}</fg #b3cfe7>: <light-white>{message}</light-white>\n"
    elif record["level"].name == "WARNING":
        return "<light-white>{time:MM-DD-YYYY HH:mm:ss}</light-white> |  <fg #b09057>{level}</fg #b09057>: <light-white>{message}</light-white>\n"
    elif record["level"].name == "SUCCESS":
        return "<light-white>{time:MM-DD-YYYY HH:mm:ss}</light-white> | <fg #6dac77>{level}</fg #6dac77>: <light-white>{message}</light-white>\n"
    elif record["level"].name == "ERROR":
        return "<light-white>{time:MM-DD-YYYY HH:mm:ss}</light-white> | <fg #a35252>{level}</fg #a35252>: <light-white>{message}</light-white>\n"
    return "<light-white>{time:MM-DD-YYYY HH:mm:ss}</light-white> | <fg #b3cfe7>{level}</fg #b3cfe7>: <light-white>{message}</light-white>\n"


def create_logger() -> logger:
    """Customer logger creation."""
    logger.remove()
    logger.add(stdout, colorize=True, catch=True, format=log_formatter)
    if ENVIRONMENT == "production":
        logger.add(
            "/var/log/broiestbot/info.json",
            format=json_formatter,
            rotation="200 MB",
            compression="zip",
            catch=True,
        )
        logger.add(
            "/var/log/broiestbot/info.log",
            colorize=True,
            catch=True,
            format=log_formatter,
            rotation="500 MB",
            compression="zip",
        )
        logger.add(
            "/var/log/broiestbot/error.log",
            colorize=True,
            catch=True,
            level="ERROR",
            format="<light-cyan>{time:MM-DD-YYYY HH:mm:ss}</light-cyan> | "
            + "<red>{level}</red>: "
            + "<light-white>{message}</light-white>",
            rotation="500 MB",
            compression="zip",
        )
    return logger


LOGGER = create_logger()
