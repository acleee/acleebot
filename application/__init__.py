"""Initialize bot module."""
import sys
from .bot import Bot
from .database import Database
from config import Config
from loguru import logger

logger.add(sys.stdout, format="{time} {level} {message}", level="INFO")


def init_bot():
    """Initiate bot."""
    db = Database(Config)
    logger.info(f'Joining {Config.chatangoRooms}')
    Bot.easy_start(rooms=Config.chatangoRooms,
                   name=Config.username,
                   password=Config.password,
                   commands=db.commands)
