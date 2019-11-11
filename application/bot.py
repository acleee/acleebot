"""Core bot logic."""
import logging
from .ch import RoomManager
from .commands.basic import send_basic_message
from .commands.scrape import scrape_random_image
from .commands.crypto import get_crypto_price
from .commands.nba import get_nba_score
from .commands.random import randomize_image
from .commands.stock import get_stock_price
from .commands.avatar import get_user_avatar
from .commands.storage import fetch_image_from_storage
from .commands.reddit import random_subreddit_image
from .commands.giphy import random_giphy_image
from .commands.urban import urban_dictionary_defintion
# from .commands.spam import spam_messages

logging.basicConfig(filename='errors.log',
                             filemode='w',
                             format='%(name)s - %(levelname)s - %(message)s',
                             level=logging.ERROR)


class Bot(RoomManager):
    """Main bot class."""

    def onInit(self):
        """Initialize bot."""
        self.setNameColor("000000")
        self.setFontColor("000000")
        self.setFontFace("Arial")
        self.setFontSize(11)

    def chat(self, row, room, args):
        """Construct a response to a valid command."""
        cmd_type = row['type']
        message = row['content']
        response = None
        if cmd_type == 'basic':
            response = send_basic_message(message)
        if cmd_type == 'scrape':
            response = scrape_random_image(message)
        if cmd_type == 'crypto':
            response = get_crypto_price(message)
        if cmd_type == 'random':
            response = randomize_image(message)
        if cmd_type == 'nba score':
            response = get_nba_score(message)
        if cmd_type == 'goal':
            logging.info('no command for goal yet.')
        if cmd_type == 'stock' and args:
            response = get_stock_price(args)
        if type == 'avi':
            response = get_user_avatar(message, args)
        if cmd_type == 'storage':
            response = fetch_image_from_storage(message)
        if cmd_type == 'reddit':
            response = random_subreddit_image(message)
        if cmd_type == 'giphy':
            response = random_giphy_image(message)
        if cmd_type == 'giphysearch' and args:
            response = random_giphy_image(args)
        if cmd_type == 'urban' and args:
            response = urban_dictionary_defintion(args)
        # if cmd_type == 'spam':
            # response = spam_messages(message)
        if response:
            logging.info(response)
            room.message(response)

    def get_command(self, message):
        """Read list of commands from database."""
        try:
            row = self.commands.loc[message]
            response = {
                'content': row['response'],
                'type': row['type']}
            return response
        except KeyError:
            logging.error(f'{message} is not a command.')

    def onMessage(self, room, user, message):
        """Boilerplate function trigger on message."""
        print("[{0}] {1}: {2}".format(room.name,
                                      user.name.title(),
                                      message.body))
        cmd = message.body.lower()
        # Trigger if chat message is a command
        if cmd[0] == "!":
            req = cmd[1::].lower()
            args = None
            if ' ' in cmd:
                req = cmd.split(' ', 1)[0][1::]
                args = cmd.split(' ', 1)[1]
            response = self.get_command(req)
            if response:
                self.chat(response, room, args)
            elif len(cmd) > 1:
                self.giphy_fallback(cmd, room, args)
        # Commands reserved to check bot status
        if cmd == 'bro?' or cmd.replace(' ', '') == '@broiestbot':
            room.message('hellouughhgughhg?')

    def giphy_fallback(self, cmd, room, args):
        """Default to Giphy for non-existant commands."""
        response = random_giphy_image(cmd)
        room.message(response)
