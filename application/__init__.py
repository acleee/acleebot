"""Initialize bot module."""
import logging
from .bot import Bot
from .db import commands_df


def init_bot(Config):
    logger = logging.basicConfig(filename='logs/errors.log',
                                 filemode='w',
                                 format='%(name)s - %(levelname)s - %(message)s',
                                 level=logging.ERROR)
    bot = Bot(commands_df,
              logger,
              Config.username,
              Config.password,
              Config.chatangoRooms)
    return bot
