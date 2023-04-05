"""Delete chats containing blacklisted phrases."""
from chatango.ch import Message, Room


def ban_word(room: Room, message: Message, user_name: str, silent=False) -> None:
    """
    Delete chat containing banned word and warn offending user.

    :param Room room: Current Chatango room object.
    :param Message message: Message sent by user.
    :param str user_name: User responsible for triggering command.
    :param bool silent: Whether offending user should be warned.

    :returns: None
    """
    message.delete()
    if silent is not True:
        room.message(f"DO NOT SAY THAT WORD @{user_name.upper()} :@")
