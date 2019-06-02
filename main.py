from application.bot import Bot
from config import username, password, testRoom, blabroom, acleeRoom


if __name__ == '__main__':
    Bot.easy_start([testRoom, acleeRoom, blabroom],
                   username,
                   password)
