"""Custom logger and error notifications."""
import json
import re
from sys import stdout

from loguru import logger

from clients import sms
from config import BASE_DIR, ENVIRONMENT, TWILIO_RECIPIENT_PHONE, TWILIO_SENDER_PHONE


def json_formatter(record: dict) -> str:
    """
    Format info message logs.

    :param dict record: Log object containing log metadata & message.

    :returns: str
    """

    def serialize_as_admin(log: dict) -> str:
        """
        Construct JSON info log record where user is room admin.

        :param dict log: Dictionary containing logged message with metadata.

        :returns: str
        """
        try:
            chat_data = re.search(
                r"(?P<room>\[\S+]) (?P<user>\[\S+]) (?P<ip>\[\S+])", log["message"]
            )
            if chat_data and log.get("message") is not None:
                chat_dict = chat_data.groupdict()
                subset = {
                    "time": log["time"].strftime("%m/%d/%Y, %H:%M:%S"),
                    "message": log["message"].split(": ", 1)[1],
                    "level": log["level"].name,
                    "room": chat_dict["room"],
                    "user": chat_dict["user"],
                    "ip": chat_dict["ip"],
                }
                return json.dumps(subset)
        except Exception as e:
            log["error"] = f"Logging error occurred: {e}"
            return serialize_error(log)

    def serialize_event(log: dict) -> str:
        """
        Construct warning log.

        :param dict log: Dictionary containing logged message with metadata.

        :returns: str
        """
        try:
            chat_data = re.search(r"(?P<room>\[\S+]) (?P<user>\[\S+])", log["message"])
            chat_dict = chat_data.groupdict()
            if (
                bool(chat_data)
                and len(chat_data.groupdict().values()) == 2
                and log.get("message") is not None
            ):
                subset = {
                    "time": log["time"].strftime("%m/%d/%Y, %H:%M:%S"),
                    "message": log["message"].split(": ", 1)[1],
                    "level": log["level"].name,
                    "room": chat_dict["room"],
                    "user": chat_dict["user"],
                }
                return json.dumps(subset)
        except Exception as e:
            log["error"] = f"Logging error occurred: {e}"
            return serialize_error(log)

    def serialize_error(log: dict) -> str:
        """
        Construct error log record.

        :param dict log: Dictionary containing logged message with metadata.

        :returns: str
        """
        if log is not None and log.get("message") is not None:
            subset = {
                "time": log["time"].strftime("%m/%d/%Y, %H:%M:%S"),
                "level": log["level"].name,
                "message": log["message"],
            }
            return json.dumps(subset)

    if record["level"].name in ("WARNING", "SUCCESS", "TRACE", "MESSAGE"):
        record["extra"]["serialized"] = serialize_event(record)
    elif record["level"].name == "INFO":
        record["extra"]["serialized"] = serialize_as_admin(record)
    else:
        record["extra"]["serialized"] = serialize_error(record)
        sms_error_handler(record)

    if record["extra"].get("serialized") is not None:
        return "{extra[serialized]},\n"


def sms_error_handler(log: dict) -> None:
    """
    Trigger error log SMS notification.

    :param dict log: Log object containing log metadata & message.
    """
    sms.messages.create(
        body=f'BROBOT ERROR: {log["time"].strftime("%m/%d/%Y, %H:%M:%S")} | {log["message"]}',
        from_=TWILIO_SENDER_PHONE,
        to=TWILIO_RECIPIENT_PHONE,
    )


def log_formatter(record: dict) -> str:
    """
    Formatter for .log records

    :param dict record: Log object containing log metadata & message.

    :returns: str
    """
    if record["level"].name == "TRACE":
        return "<fg #70acde>{time:MM-DD-YYYY HH:mm:ss}</fg #70acde> | <fg #cfe2f3>{level}</fg #cfe2f3>: <light-white>{message}</light-white>\n"
    elif record["level"].name == "INFO":
        return "<fg #70acde>{time:MM-DD-YYYY HH:mm:ss}</fg #70acde> | <fg #9cbfdd>{level}</fg #9cbfdd>: <light-white>{message}</light-white>\n"
    elif record["level"].name == "DEBUG":
        return "<fg #70acde>{time:MM-DD-YYYY HH:mm:ss}</fg #70acde> | <fg #8598ea>{level}</fg #8598ea>: <light-white>{message}</light-white>\n"
    elif record["level"].name == "WARNING":
        return "<fg #70acde>{time:MM-DD-YYYY HH:mm:ss}</fg #70acde> |  <fg #dcad5a>{level}</fg #dcad5a>: <light-white>{message}</light-white>\n"
    elif record["level"].name == "SUCCESS":
        return "<fg #70acde>{time:MM-DD-YYYY HH:mm:ss}</fg #70acde> | <fg #3dd08d>{level}</fg #3dd08d>: <light-white>{message}</light-white>\n"
    elif record["level"].name == "ERROR":
        return "<fg #70acde>{time:MM-DD-YYYY HH:mm:ss}</fg #70acde> | <fg #ae2c2c>{level}</fg #ae2c2c>: <light-white>{message}</light-white>\n"
    return "<fg #70acde>{time:MM-DD-YYYY HH:mm:ss}</fg #70acde> | <fg #b3cfe7>{level}</fg #b3cfe7>: <light-white>{message}</light-white>\n"


def create_logger() -> logger:
    """
    Configure custom logger.

    :returns: logger
    """
    logger.remove()
    logger.add(stdout, colorize=True, catch=True, format=log_formatter)
    if ENVIRONMENT == "production":
        logger.add(
            "/var/log/broiestbot/info.json",
            format=json_formatter,
            rotation="300 MB",
            compression="zip",
            catch=True,
        )
        logger.add(
            "/var/log/broiestbot/info.log",
            colorize=True,
            catch=True,
            format=log_formatter,
            rotation="300 MB",
            compression="zip",
        )
        logger.add(
            "/var/log/broiestbot/error.log",
            colorize=True,
            catch=True,
            level="ERROR",
            format="<fg #70acde>{time:MM-DD-YYYY HH:mm:ss}</fg #70acde> | "
            + "<red>{level}</red>: "
            + "<light-white>{message}</light-white>",
            rotation="300 MB",
            compression="zip",
        )
    elif ENVIRONMENT == "development":
        logger.add(
            f"{BASE_DIR}/logs/error.log",
            colorize=True,
            level="ERROR",
            format="<fg #70acde>{time:MM-DD-YYYY HH:mm:ss}</fg #70acde> | "
            + "<red>{level}</red>: "
            + "<light-white>{message}</light-white>",
            rotation="300 MB",
            compression="zip",
        )
        logger.add(
            f"{BASE_DIR}/logs/error.json",
            level="ERROR",
            format=json_formatter,
            rotation="300 MB",
            compression="zip",
        )
    return logger


LOGGER = create_logger()
