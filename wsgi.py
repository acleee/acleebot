"""Bot application entry point."""
from broiestbot import join_rooms
from config import CHATANGO_USERS, ENVIRONMENT

init_bot = join_rooms(
        ENVIRONMENT,
        CHATANGO_USERS["BROIESTBRO"]["USERNAME"],
        CHATANGO_USERS["BROIESTBRO"]["PASSWORD"],
    )

if __name__ == "__main__":
    init_bot
