"""Custom logger and error notifications."""
import json
import re
from sys import stdout

from loguru import logger


from clients import sms
from config import BASE_DIR, ENVIRONMENT, TWILIO_BRO_PHONE_NUMBER, TWILIO_SENDER_PHONE


DD_APM_FORMAT = (
    "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] "
    "[dd.service=%(dd.service)s dd.env=%(dd.env)s "
    "dd.version=%(dd.version)s "
    "dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s]"
    "- %(message)s"
)


def json_formatter(record: dict) -> str:
    """
    Format info message logs.

    :param dict record: Log object containing log metadata & message.

    :returns: str
    """

    record["time"] = record["time"].strftime("%m/%d/%Y, %H:%M:%S")
    record["elapsed"] = record["elapsed"].total_seconds()

    def serialize_as_admin(log: dict) -> str:
        """
        Construct JSON info log record where user is room admin.

        :param dict log: Dictionary containing logged message with metadata.

        :returns: str
        """
        try:
            chat_data = re.search(r"(?P<room>\[\S+]) (?P<user>\[\S+]) (?P<ip>\[\S+])", log.get("message"))
            if chat_data and log.get("message"):
                subset = {
                    "time": log["time"],
                    "message": log["message"].split(": ", 1)[1],
                    "level": log["level"].name,
                    "room": chat_data["room"].replace("[", "").replace("]", ""),
                    "user": chat_data["user"].replace("[", "").replace("]", ""),
                    "ip": chat_data["ip"].replace("[", "").replace("]", ""),
                }
                return json.dumps(subset)
        except Exception as e:
            subset["error"] = f"Logging error occurred: {str(e)}"
            return serialize_error(subset)

    def serialize_event(log: dict) -> str:
        """
        Construct warning log.

        :param dict log: Dictionary containing logged message with metadata.

        :returns: str
        """
        try:
            chat_data = re.search(r"(?P<room>\[\S+]) (?P<user>\[\S+])", log["message"])
            if bool(chat_data) and log.get("message") is not None:
                subset = {
                    "time": log["time"],
                    "message": log["message"].split(": ", 1)[1],
                    "level": log["level"].name,
                    "room": chat_data["room"].replace("[", "").replace("]", ""),
                    "user": chat_data["user"].replace("[", "").replace("]", ""),
                }
                return json.dumps(subset)
        except Exception as e:
            log["error"] = f"Logging error occurred: {str(e)}"

    def serialize_error(log: dict) -> str:
        """
        Construct error log record.

        :param dict log: Dictionary containing logged message with metadata.

        :returns: str
        """
        if log and log.get("message"):
            subset = {
                "time": log["time"],
                "level": log["level"].name,
                "message": log["message"],
            }
            return json.dumps(subset)

    if record["level"].name == "INFO":
        record["extra"]["serialized"] = serialize_as_admin(record)
        return "{extra[serialized]},\n"
    elif record["level"].name in ("WARNING", "SUCCESS"):
        record["extra"]["serialized"] = serialize_event(record)
        return "{extra[serialized]},\n"
    else:
        record["extra"]["serialized"] = serialize_error(record)
        sms_error_handler(record)
        return "{extra[serialized]},\n"


def sms_error_handler(log: dict) -> None:
    """
    Trigger error log SMS notification.

    :param dict log: Log object containing log metadata & message.

    :returns: None
    """
    sms.messages.create(
        body=f'BROBOT ERROR: {log["time"].strftime("%m/%d/%Y, %H:%M:%S")} | {log["message"]}',
        from_=TWILIO_SENDER_PHONE,
        to=TWILIO_BRO_PHONE_NUMBER,
    )


def log_formatter(record: dict) -> str:
    """
    Formatter for .log records
    :param dict record: Key/value object containing a single log's message & metadata.
    :returns: str
    """
    if record["level"].name == "INFO":
        return "<fg #5278a3>{time:MM-DD-YYYY HH:mm:ss}</fg #5278a3> | <fg #b3cfe7>{level}</fg #b3cfe7>: <light-white>{message}</light-white>\n"
    elif record["level"].name == "WARNING":
        return "<fg #5278a3>{time:MM-DD-YYYY HH:mm:ss}</fg #5278a3> |  <fg #b09057>{level}</fg #b09057>: <light-white>{message}</light-white>\n"
    elif record["level"].name == "SUCCESS":
        return "<fg #5278a3>{time:MM-DD-YYYY HH:mm:ss}</fg #5278a3> | <fg #6dac77>{level}</fg #6dac77>: <light-white>{message}</light-white>\n"
    elif record["level"].name == "ERROR":
        return "<fg #5278a3>{time:MM-DD-YYYY HH:mm:ss}</fg #5278a3> | <fg #a35252>{level}</fg #a35252>: <light-white>{message}</light-white>\n"
    return "<fg #5278a3>{time:MM-DD-YYYY HH:mm:ss}</fg #5278a3> | <fg #b3cfe7>{level}</fg #b3cfe7>: <light-white>{message}</light-white>\n"


def create_logger() -> logger:
    """
    Configure custom logger.
    :returns: logger
    """
    logger.remove()
    logger.add(stdout, colorize=True, catch=True, format=log_formatter)
    if ENVIRONMENT == "production":
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
            format=log_formatter,
            rotation="300 MB",
            compression="zip",
        )
        # Datadog JSON logs
        logger.add(
            "/var/log/broiestbot/info.json",
            format=json_formatter,
            rotation="300 MB",
            compression="zip",
        )
        # Datadog APM tracing
        logger.add(
            "/var/log/broiestbot/apm.json",
            serialize=True,
            catch=True,
            format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
            rotation="300 MB",
            compression="zip",
        )
    elif ENVIRONMENT == "development":
        logger.add(
            f"{BASE_DIR}/logs/info.log",
            colorize=True,
            catch=True,
            format=log_formatter,
            rotation="300 MB",
            compression="zip",
        )
        # Datadog APM tracing
        logger.add(
            f"{BASE_DIR}/logs/apm.json",
            serialize=True,
            catch=True,
            format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
            rotation="300 MB",
            compression="zip",
        )
        # Datadog JSON logs
        logger.add(
            f"{BASE_DIR}/logs/info.json",
            format=json_formatter,
            rotation="300 MB",
            compression="zip",
        )
    return logger


LOGGER = create_logger()
