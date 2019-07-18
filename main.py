from application.bot import Bot
from config import username, password, testRoom, blabRoom, acleeRoom, sixersRoom, philliesRoom


if __name__ == '__main__':
    Bot.easy_start([testRoom, acleeRoom, blabRoom, sixersRoom, philliesRoom],
                   username,
                   password)
