"""Initialize bot."""
from multiprocessing import Process

from datadog import initialize

from broiestbot.bot import Bot
from config import CHATANGO_ROOMS, CHATANGO_TEST_ROOM


def join_rooms(environment: str, user: str, password: str):
    """
    Create bot instance for single Chatango room.

    :param str environment: Env to run bot in.
    :param str user: Chatango username to authenticate as.
    :param str password: Chatango password for authentication.
    """
    if environment == "development":
        start_bot_development_mode(user, password)
    else:
        start_bot_production_mode(user, password)


def start_bot_development_mode(user: str, password: str):
    """
    Initialize bot in development room for testing purposes.

    :param str user: Chatango username to authenticate as.
    :param str password: Chatango password for authentication.
    """
    p = Process(
        target=Bot.easy_start,
        kwargs={
            "rooms": CHATANGO_TEST_ROOM,
            "name": user,
            "password": password,
        },
    )
    p.start()
    p.join()


def start_bot_production_mode(user: str, password: str):
    """
    Join all production rooms.

    :param str user: Chatango username to authenticate as.
    :param str password: Chatango password for authentication.
    """
    options = {"statsd_host": "127.0.0.1", "statsd_port": 8125}
    initialize(**options)
    print(f'Joining {", ".join(CHATANGO_ROOMS)}')
    for room in CHATANGO_ROOMS:
        p = Process(
            target=Bot.easy_start,
            kwargs={
                "rooms": [room],
                "name": user,
                "password": password,
            },
        )
        p.start()
        p.join()
