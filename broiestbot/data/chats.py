"""Persist chat logs."""
from database import session_rw
from database.models import Chat
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from config import PERSIST_CHAT_DATA
from logger import LOGGER


def persist_chat_logs(user_name: str, room_name: str, chat_message: str, bot_username: str) -> None:
    """
    Save chat log record.

    :param str user_name: Chatango username of chatter.
    :param str room_name: Chatango room where chat occurred.
    :param str chat_message: Content of the chat.
    :param str bot_username: Name of the currently run bot.

    :returns: None
    """
    try:
        if PERSIST_CHAT_DATA == "true" and bot_username in ("broiestbro", "broiestbot"):
            session_rw.add(Chat(username=user_name, room=room_name, message=chat_message))
    except IntegrityError as e:
        LOGGER.warning(f"Failed to save duplicate chat entry: {e}")
    except SQLAlchemyError as e:
        LOGGER.warning(f"SQLAlchemyError occurred while persisting chat data from  {user_name}, `{chat_message}`: {e}")
    except Exception as e:
        LOGGER.warning(f"Unexpected error occurred while persisting chat data from {user_name}, `{chat_message}`: {e}")
