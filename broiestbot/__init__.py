"""Initialize bot."""
from broiestbot.bot import Bot
from broiestbot.clients import db
from config import (
    CHATANGO_BRO_USERNAME,
    CHATANGO_BRO_PASSWORD,
    DATABASE_COMMANDS_TABLE,
    DATABASE_WEATHER_TABLE,
    CHATANGO_ROOMS,
    CHATANGO_TEST_ROOM,
    ENVIRONMENT
)


def join_room(rooms):
    """Create bot instance for single Chatango room."""
    commands = db.get_table(DATABASE_COMMANDS_TABLE, 'id')
    weather = db.get_table(DATABASE_WEATHER_TABLE, 'code')
    chat_bot = Bot.easy_start(
        rooms=rooms,
        name=CHATANGO_BRO_USERNAME,
        password=CHATANGO_BRO_PASSWORD,
        commands=commands,
        weather=weather
    )
    chat_bot.create_message('basic', 'Beep boop I\'m dead inside 🤖')


def start_bot():
    """Initialize bot depending on environment."""
    if ENVIRONMENT == 'development':
        print('Starting in dev mode...')
        join_room([CHATANGO_TEST_ROOM])
    else:
        print(f'Joining {", ".join(CHATANGO_ROOMS)}')
        join_room(CHATANGO_ROOMS)

    return len(f'Joined {len(CHATANGO_ROOMS)} rooms.')

