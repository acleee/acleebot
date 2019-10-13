"""Core bot logic."""
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
from .commands.spam import spam_messages
from .commands.channel import channel


class Bot(RoomManager):
    """Main bot class."""

    def __init__(self, commands_df, logger, username, password, rooms):
        self.commands_df = commands_df
        self.logger = logger
        self.easy_start(rooms, username, password)

    def onInit(self):
        """Initialize bot."""
        self.setNameColor("000000")
        self.setFontColor("000000")
        self.setFontFace("Arial")
        self.setFontSize(11)

    def chat(self, row, room, args):
        """Construct a response to a valid command."""
        type = row['type']
        message = row['content']
        response = 'under development tbh'
        if type == 'basic':
            response = send_basic_message(message)
        if type == 'scrape':
            response = scrape_random_image(message)
        if type == 'crypto':
            response = get_crypto_price(message)
        if type == 'random':
            response = randomize_image(message)
        if type == 'nba score':
            response = get_nba_score(message)
        if type == 'goal':
            self.logger.info('no command for goal yet.')
        if type == 'stock' and args:
            response = get_stock_price(args)
        if type == 'avi':
            response = get_user_avatar(message)
        if type == 'storage':
            response = fetch_image_from_storage(message)
        if type == 'reddit':
            response = random_subreddit_image(message)
        if type == 'giphy':
            response = random_giphy_image(message)
        if type == 'giphysearch' and args:
            response = random_giphy_image(args)
        if type == 'urban' and args:
            response = urban_dictionary_defintion(args)
        if type == 'spam':
            response = spam_messages(message)
        if type == 'channel':
            response = channel(message)
        room.message(response)

    def get_command(self, message):
        """Read list of commands from database."""
        try:
            row = self.commands_df.loc[message]
            response = {
                'content': row['response'],
                'type': row['type']}
            return response
        except KeyError:
            self.logger.error(f'{message} is not a command.')

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
        # Commands reserved to check bot status
        if cmd == 'bro?' or cmd.replace(' ', '') == '@broiestbot':
            room.message('hellouughhgughhg?')
