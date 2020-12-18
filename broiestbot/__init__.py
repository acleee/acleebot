"""Initialize bot."""
from datadog import initialize

from broiestbot.bot import Bot
from clients import db
from config import (
    CHATANGO_BRO_PASSWORD,
    CHATANGO_BRO_USERNAME,
    CHATANGO_ROOMS,
    CHATANGO_TEST_ROOM,
    DATABASE_COMMANDS_TABLE,
    DATABASE_WEATHER_TABLE,
    ENVIRONMENT,
)


def join_rooms(rooms):
    """Create bot instance for single Chatango room."""
    commands = db.get_table(DATABASE_COMMANDS_TABLE, "id")
    weather = db.get_table(DATABASE_WEATHER_TABLE, "id")
    chat_bot = Bot.easy_start(
        rooms=rooms,
        name=CHATANGO_BRO_USERNAME,
        password=CHATANGO_BRO_PASSWORD,
        commands=commands,
        weather=weather,
    )
    chat_bot.create_message("basic", "Beep boop I'm dead inside 🤖")


def start_bot():
    """Initialize bot depending on environment."""
    if ENVIRONMENT == "development":
        print("Starting in dev mode...")
        join_rooms([CHATANGO_TEST_ROOM])
    else:
        options = {"statsd_host": "127.0.0.1", "statsd_port": 8125}
        initialize(**options)
        print(f'Joining {", ".join(CHATANGO_ROOMS)}')
        join_rooms(CHATANGO_ROOMS)

    return len(f"Joined {len(CHATANGO_ROOMS)} rooms.")
