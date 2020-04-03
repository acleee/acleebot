"""Initialize bot module."""
from .bot import Bot
from .google_storage import GCS
from .tables import commands, weather
from config import (CHATANGO_USERNAME,
                    CHATANGO_PASSWORD)


def start_bot(room):
    """Join Chatango room on dedicated CPU thread."""
    Bot.easy_start(rooms=[room],
                   name=CHATANGO_USERNAME,
                   password=CHATANGO_PASSWORD,
                   commands=commands)
