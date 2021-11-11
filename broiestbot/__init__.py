"""Initialize bot."""
from multiprocessing import Process
from typing import List

from datadog import initialize

from broiestbot.bot import Bot
from config import CHATANGO_ROOMS, CHATANGO_TEST_ROOM, CHATANGO_USERS


def join_rooms(rooms: List[str]):
    """
    Create bot instance for single Chatango room.

    :param List[str] rooms: Chatango rooms to join.
    """
    for room in rooms:
        p = Process(
            target=Bot.easy_start,
            kwargs={
                "rooms": room,
                "name": CHATANGO_USERS["BROIESTBRO"]["USERNAME"],
                "password": CHATANGO_USERS["BROIESTBRO"]["PASSWORD"],
            },
        )
        p.start()
        p.join()


def start_bot_development_mode():
    """Initialize bot depending on environment."""
    p = Process(
        target=Bot.easy_start,
        kwargs={
            "rooms": [CHATANGO_TEST_ROOM],
            "name": CHATANGO_USERS["BROIESTBRO"]["USERNAME"],
            "password": CHATANGO_USERS["BROIESTBRO"]["PASSWORD"],
        },
    )
    p.start()
    p.join()


def start_bot_production_mode():
    options = {"statsd_host": "127.0.0.1", "statsd_port": 8125}
    initialize(**options)
    print(f'Joining {", ".join(CHATANGO_ROOMS)}')
    for room in CHATANGO_ROOMS:
        p = Process(
            target=Bot.easy_start,
            kwargs={
                "rooms": room,
                "name": CHATANGO_USERS["BROIESTBRO"]["USERNAME"],
                "password": CHATANGO_USERS["BROIESTBRO"]["PASSWORD"],
            },
        )
        p.start()
        p.join()
