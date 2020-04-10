"""Initialize bot module."""
from .bot import Bot
from .tables import commands
from config import (CHATANGO_USERNAME,
                    CHATANGO_PASSWORD)


def start_bot(room):
    """Initialize bot instance for a single room."""
    Bot.easy_start(rooms=room,
                   name=CHATANGO_USERNAME,
                   password=CHATANGO_PASSWORD,
                   commands=commands)
