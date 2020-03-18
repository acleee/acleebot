"""Initialize bot module."""
import sys
from .bot import Bot
from .database import Database
from .google_storage import GCS
from .charts import create_chart
from config import Config
from loguru import logger


logger.add(sys.stdout, format="{time} {level} {message}", level="INFO")


def init_bot():
    """Initiate bot."""
    db = Database(Config)
    create_chart(db.get_market_data('DJI'), 'DJI', 'Dow Jones Industrial Avg.')
    logger.info(f'Joining {Config.CHATANGO_ROOMS}')
    Bot.easy_start(rooms=Config.CHATANGO_ROOMS,
                   name=Config.CHATANGO_USERNAME,
                   password=Config.CHATANGO_PASSWORD,
                   commands=db.commands)
