"""Core bot logic."""
import sys
from loguru import logger
from .ch import RoomManager
from .commands import (basic_message,
                       get_crypto_price,
                       random_image,
                       get_stock_price,
                       get_user_avatar,
                       fetch_image_from_gcs,
                       giphy_image_search,
                       urban_dictionary_defintion)

logger.add('logs/info.log',
           format="{time} {level} {message}",
           level="INFO",
           catch=False)
logger.add(sys.stdout,
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
        # self.create_message('basic', 'Beep boop I\'m dead inside 🤖')

    @staticmethod
    def chat(room, message):
        """Construct a response to a valid command."""
        room.message(message)

    @staticmethod
    def create_message(cmd, content, args=None):
        response = None
        if cmd == 'basic':
            response = basic_message(content)
        if cmd == 'crypto':
            response = get_crypto_price(cmd, content)
        if cmd == 'random':
            response = random_image(content)
        if cmd == 'stock' and args:
            response = get_stock_price(args)
        if cmd == 'avi':
            response = get_user_avatar(content, args)
        if cmd == 'storage':
            response = fetch_image_from_gcs(content)
        if cmd == 'giphy':
            response = giphy_image_search(content)
        if cmd == 'urban' and args:
            response = urban_dictionary_defintion(args)
        return response

    @logger.catch
    def get_command(self, message):
        """Read commands from database."""
        try:
            row = self.commands.loc[message]
            response = {
                'content': row['response'],
                'type': row['type']}
            return response
        except KeyError:
            logger.error(f'{message} is not a command.')

    @logger.catch
    def onMessage(self, room, user, message):
        """Boilerplate function trigger on message."""
        logger.info("[{0}] {1} ({2}): {3}".format(room.name,
                                                  user.name.title(),
                                                  message.ip,
                                                  message.body))
        user_msg = message.body.lower()
        # Trigger if chat message is a command
        if user_msg[0] == "!":
            self.command_response(user_msg, room)
        elif user_msg == 'bro?' or user_msg.replace(' ', '') == '@broiestbot':
            self.bot_status_check(room)
        elif 'blab' in user_msg and 'south' not in user_msg:
            self.banned_word(room, message, user)
        elif user_msg.endswith('only on aclee'):
            self.chat(room, '™')

    @logger.catch
    def command_response(self, cmd, room):
        """Respond to command."""
        print('cmd = ', cmd)
        req = cmd[1::].lower()
        args = None
        if ' ' in cmd:
            req = cmd.split(' ', 1)[0][1::]
            args = cmd.split(' ', 1)[1]
        command = self.get_command(req)
        if command:
            message = self.create_message(command['type'], command['content'], args=args)
            if message:
                self.chat(room, message)
        else:
            self.giphy_fallback(cmd, room)

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
        room.message(f"DO NOT SAY THAT WORD @{user.name.upper()} :@")

    @staticmethod
    def trademarked(room):
        """ONLY on ACLEE™"""
        room.message('™')
