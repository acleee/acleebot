from typing import Optional

from emoji import emojize

from chatango.ch import Message, Room
from config import (
    CHATANGO_BLACKLISTED_USERS,
    CHATANGO_BANNED_IPS,
    CHATANGO_EGGSER_USERNAME_WHITELIST,
    CHATANGO_IGNORED_IPS,
    CHATANGO_IGNORED_USERS,
    CHATANGO_BLACKLIST_ROOMS,
)
from logger import LOGGER

from .ban import ban_user


def check_blacklisted_users(room: Room, user_name: str, message: Message) -> None:
    """
    Ban and delete chat history of blacklisted user.

    :param Room room: Chatango room in which user appeared.
    :param str user_name: Chatango username to validate against blacklist.
    :param Message message: User submitted message.

    :returns: None
    """
    if user_name in CHATANGO_BLACKLISTED_USERS and room.room_name.lower() in CHATANGO_BLACKLIST_ROOMS:
        reply = emojize(f":wave: @{user_name} lmao pz fgt have fun being banned forever :wave:", language="en")
        LOGGER.warning(f"BANNED user: username={message.user.name} ip={message.ip}")
        room.message(reply)
        room.clear_user(message.user)
        room.ban_user(message.user)
    elif (
        message.ip is not None
        and message.ip in CHATANGO_BANNED_IPS
        and message.user.name.lower() not in CHATANGO_EGGSER_USERNAME_WHITELIST
    ):
        ban_user(room, message)
    elif is_user_anon(user_name) and "raiders" in message.body.lower():
        ban_user(room, message)
    elif is_user_anon(user_name) and "tigger" in message.body.lower():
        ban_user(room, message)
    elif is_user_anon(user_name) and "wordle" in message.body.lower():
        ban_user(room, message)
    elif "wordle" in message.body.lower() and "tomorrow" in message.body.lower():
        ban_user(room, message)
    elif "is the wordle" in message.body.lower():
        ban_user(room, message)


def check_ignored_users(user_name: str, user_ip: str) -> Optional[str]:
    """
    Ignore commands from users who have had bot privileges revokes

    :param str user_name: Chatango username to validate against blacklist.
    :param str user_ip: IP address of Chatango user to validate against blacklist.

    :returns: str
    """
    if user_name in CHATANGO_IGNORED_USERS or user_ip in CHATANGO_IGNORED_IPS:
        return emojize(
            f":wave: @{user_name} bot privileges REVOKED for acting like a CUNT :wave:",
            language="en",
        )
    return None


def is_user_anon(user_name: str) -> bool:
    """
    Check whether user is anon.

    :param str user_name: Chatango username to validate as anon.

    :returns: bool
    """
    if "!anon" in user_name or "#" in user_name:
        return True
    return False
