"""Ban a user from a room and delete their chat history."""
from chatango.ch import Message, Room
from logger import LOGGER


def ban_user(room: Room, message: Message) -> None:
    """
    Ban and delete chat history of a user.

    :param Room room: Chatango room object.
    :param Message message: User submitted message.

    :returns: None
    """
    LOGGER.warning(f"BANNED user: username={message.user.name} ip={message.ip}")
    room.clear_user(message.user)
    room.ban_user(message.user)
