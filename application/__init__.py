"""Initialize bot module."""
from .bot import Bot


def init_bot(Config):
    """Starts bot."""
    print(f'Joining {Config.chatangoRooms}')
    Bot.easy_start(rooms=Config.chatangoRooms,
                   name=Config.username,
                   password=Config.password)
