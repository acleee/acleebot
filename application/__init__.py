"""Initialize bot module."""
from .bot import Bot
from .database import Database
from .google_storage import GCS
from .cmd import Commands
from config import (CHATANGO_USERNAME,
                    CHATANGO_PASSWORD,
                    DATABASE_COMMANDS_TABLE,
                    DATABASE_URI,
                    DATABASE_ARGS)


def start_bot(room):
    """Join Chatango room on dedicated CPU thread."""
    db = Database(DATABASE_COMMANDS_TABLE, DATABASE_URI, DATABASE_ARGS)
    commands = Commands(db.commands)
    Bot.easy_start(rooms=[room],
                   name=CHATANGO_USERNAME,
                   password=CHATANGO_PASSWORD,
                   commands=commands)
