"""Initialize bot."""
from multiprocessing import Process
from broiestbot.bot import Bot
from broiestbot.clients import db
from config import (
    CHATANGO_USERNAME,
    CHATANGO_PASSWORD,
    DATABASE_COMMANDS_TABLE,
    DATABASE_WEATHER_TABLE,
    CHATANGO_ROOMS,
    CHATANGO_TEST_ROOM,
    ENVIRONMENT
)


def join_room(room):
    """Initialize bot instance for a single room."""
    print(f'Joining {room}...')
    commands = db.get_table(DATABASE_COMMANDS_TABLE, 'command')
    weather = db.get_table(DATABASE_WEATHER_TABLE, 'code')
    chat_bot = Bot.easy_start(
        rooms=[room],
        name=CHATANGO_USERNAME,
        password=CHATANGO_PASSWORD,
        commands=commands,
        weather=weather
    )
    chat_bot.create_message('basic', 'Beep boop I\'m dead inside 🤖')


def start_bot():
    """Dedicate a single process per bot."""
    if ENVIRONMENT == 'development':
        print('Starting in dev mode...')
        join_room(CHATANGO_TEST_ROOM)
    else:
        processes = []
        for room in CHATANGO_ROOMS:
            p = Process(target=join_room, args=(room,))
            processes.append(p)
            p.start()
        for process in processes:
            process.join()

    return len(f'Joined {len(CHATANGO_ROOMS)} rooms.')

