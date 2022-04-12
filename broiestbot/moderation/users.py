from emoji import emojize

from chatango.ch import Message, Room
from config import (
    CHATANGO_BLACKLISTED_USERS,
    CHATANGO_EGGSER_IP,
    CHATANGO_EGGSER_USERNAME_WHITELIST,
)
from logger import LOGGER

from .ban import ban_user


def check_blacklisted_users(room: Room, user_name: str, message: Message) -> None:
    """
    Ban and delete chat history of blacklisted user.

    :param Room room: Chatango room object.
    :param str user_name: Chatango username to validate against blacklist.
    :param Message message: User submitted message.

    :returns: None
    """
    if user_name in CHATANGO_BLACKLISTED_USERS:
        reply = emojize(
            f":wave: @{user_name} lmao pz fgt have fun being banned forever :wave:",
            use_aliases=True,
        )
        LOGGER.warning(f"BANNED user: username={message.user.name} ip={message.ip}")
        room.message(reply)
        room.clear_user(message.user)
        room.ban_user(message.user)
    elif (
        message.ip is not None
        and message.ip.startswith(CHATANGO_EGGSER_IP)
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


def is_user_anon(user_name: str) -> bool:
    """
    Check whether user is anon.

    :param str user_name: Chatango username to validate as anon.

    :returns: bool
    """
    if "!anon" in user_name or "#" in user_name:
        return True
    return False
