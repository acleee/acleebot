"""Initialize bot module."""
from .bot import Bot
from .database import Database
from config import Config

db = Database(Config)


def init_bot():
    """Starts bot."""
    print(f'Joining {Config.chatangoRooms}')
    Bot.easy_start(rooms=Config.chatangoRooms,
                   name=Config.username,
                   password=Config.password,
                   commands=db.commands)
