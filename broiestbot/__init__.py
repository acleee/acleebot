"""Initialize bot."""
from typing import List

from datadog import initialize

from broiestbot.bot import Bot
from config import CHATANGO_ROOMS, CHATANGO_TEST_ROOM, CHATANGO_USERS, ENVIRONMENT


def join_rooms(rooms: List[str]):
    """
    Create bot instance for single Chatango room.

    :param List[str] rooms: Chatango rooms to join.
    """
    while True:
        broiestbot = Bot(
            CHATANGO_USERS["BROIESTBRO"]["USERNAME"],
            CHATANGO_USERS["BROIESTBRO"]["PASSWORD"],
        )
        try:
            for room in rooms:
                broiestbot.join_room(room)
            broiestbot.main()
        except KeyboardInterrupt as e:
            broiestbot.stop()
            print(f"KeyboardInterrupt while joining Chatango room: {e}")
            break
        except Exception as e:
            broiestbot.stop()
            print(f"Unexpected exception while joining Chatango room: {e}")
            break


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
