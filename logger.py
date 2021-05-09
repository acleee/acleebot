"""Custom logger and error notifications."""
import re
from sys import stdout

import simplejson as json
from loguru import logger

from clients import sms
from config import ENVIRONMENT, TWILIO_RECIPIENT_PHONE, TWILIO_SENDER_PHONE


def formatter(record: dict):
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

    if record["level"].name in ("WARNING", "SUCCESS", "TRACE"):
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
