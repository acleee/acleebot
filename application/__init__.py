"""Initialize bot."""
from .bot import Bot
from application.database import Database
from config import (CHATANGO_USERNAME,
                    CHATANGO_PASSWORD,
                    DATABASE_URI,
                    DATABASE_COMMANDS_TABLE,
                    DATABASE_WEATHER_TABLE,
                    DATABASE_ARGS)

db = Database(DATABASE_URI, DATABASE_ARGS)


def start_bot(room):
    """Initialize bot instance for a single room."""
    print(f'Joining {room}...')
    commands = db.get_table(DATABASE_COMMANDS_TABLE, 'command')
    weather = db.get_table(DATABASE_WEATHER_TABLE, 'code')
    chatbot = Bot.easy_start(rooms=[room],
                             name=CHATANGO_USERNAME,
                             password=CHATANGO_PASSWORD,
                             commands=commands,
                             weather=weather)
