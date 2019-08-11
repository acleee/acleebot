from application.bot import Bot
from config import username, password, chatangoRooms

if __name__ == '__main__':
    Bot.easy_start(chatangoRooms,
                   username,
                   password)
