"""Core bot logic."""
import re
from loguru import logger
from .ch import RoomManager
from .logic import (basic_message,
                    get_crypto_price,
                    random_image,
                    stock_price_chart,
                    fetch_image_from_gcs,
                    giphy_image_search,
                    urban_dictionary,
                    nba_team_score,
                    subreddit_image,
                    weather_by_city,
                    wiki_summary)

logger.add('logs/info.log',
           format="{time} {level} {message}",
           level="INFO",
           catch=False)
logger.add('logs/errors.log',
           format="{time} {level} {message}",
           level="ERROR",
           catch=True)


class Bot(RoomManager):

    def onInit(self):
        """Initialize bot."""
        self.setNameColor("000000")
        self.setFontColor("000000")
        self.setFontFace("Arial")
        self.setFontSize(11)
        self.create_message('basic', 'Beep boop I\'m dead inside 🤖')

    @staticmethod
    def _chat(room, message):
        """Construct a response to a valid command."""
        room.message(message)

    @staticmethod
    def create_message(type, content, command=None, args=None):
        response = None
        if type == 'basic':
            response = basic_message(content)
        elif type == 'crypto':
            response = get_crypto_price(command, content)
        elif type == 'random':
            response = random_image(content)
        elif type == 'stock' and args:
            response = stock_price_chart(args)
        elif type == 'avi':
            response = get_user_avatar(content, args)
        elif type == 'storage':
            response = fetch_image_from_gcs(content)
        elif type == 'giphy':
            response = giphy_image_search(content)
        elif type == 'urban' and args:
            response = urban_dictionary(args)
        elif type == 'nba' and args:
            response = nba_team_score(args)
        elif type == 'reddit':
            response = subreddit_image(content)
        elif type == 'weather' and args:
            response = weather_by_city(args)
        elif type == 'wiki' and args:
            response = wiki_summary(args)
        return response

    @logger.catch
    def onMessage(self, room, user, message):
        """Boilerplate function trigger on message."""
        logger.info("[{0}] {1} ({2}): {3}".format(room.name,
                                                  user.name.title(),
                                                  message.ip,
                                                  message.body))
        user_msg = message.body.lower()
        print(user_msg)
        if user_msg[0] == "!":
            self.command_response(user_msg, room)  # Trigger if message is a command
        elif user_msg == 'bro?':
            self.bot_status_check(room)
        elif user_msg.endswith('only on aclee'):
            self._chat(room, '™')
        elif user_msg.lower() == 'tm':
            self.replace_word(room, message)
        elif re.search('bl(\S+)b', user_msg) and 'south' not in user_msg:
            self.banned_word(room, message, user)

    @logger.catch
    def command_response(self, user_msg, room):
        """Respond to command."""
        user_msg = user_msg[1::].lower()
        args = None
        if ' ' not in user_msg:
            cmd = user_msg
        else:
            cmd = user_msg.split(' ', 1)[0]
            args = user_msg.split(' ', 1)[1]
        command = self.commands.get(cmd)
        if command is not None:
            message = self.create_message(command['type'],
                                          command['response'],
                                          command=cmd,
                                          args=args)
            if message:
                self._chat(room, message)
        else:
            self.giphy_fallback(user_msg, room)

    @staticmethod
    def bot_status_check(room):
        """Check bot status."""
        room.message('hellouughhgughhg?')

    @staticmethod
    def giphy_fallback(cmd, room):
        """Default to Giphy for non-existent commands."""
        cmd = cmd.replace('!', '')
        if len(cmd) > 1:
            response = giphy_image_search(cmd)
            room.message(response)

    @staticmethod
    def banned_word(room, message, user):
        """Remove banned words."""
        message.delete()
        room.message(f'DO NOT SAY THAT WORD @{user.name.upper()} :@')

    @staticmethod
    def replace_word(room, message):
        """Remove banned words."""
        message.delete()
        room.message("™")
