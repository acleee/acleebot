"""Bot application entry point."""
from broiestbot import join_rooms
from config import CHATANGO_USERS, ENVIRONMENT

if __name__ == "__main__":
    join_rooms(
        ENVIRONMENT,
        CHATANGO_USERS["BROIESTBRO"]["USERNAME"],
        CHATANGO_USERS["BROIESTBRO"]["PASSWORD"],
    )
