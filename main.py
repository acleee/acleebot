from application.bot import Bot
from config import username, password, testRoom, blabRoom, acleeRoom, sixersRoom


if __name__ == '__main__':
    Bot.easy_start([testRoom, acleeRoom, blabRoom, sixersRoom],
                   username,
                   password)
