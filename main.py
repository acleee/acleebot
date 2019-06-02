from application.bot import Bot
from config import username, password, testRoom, blabroom, acleeRoom


def main():
    Bot.easy_start([testRoom, acleeRoom, blabroom],
                   username,
                   password)
