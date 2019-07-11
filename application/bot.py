"""Core bot logic."""
from . import ch
from . import db
from .commands.basic import send_basic_message
from .commands.scrape import scrape_random_image
from .commands.crypto import get_crypto_price
from .commands.nba import get_nba_score
from .commands.random import randomize_image
from .commands.stock import get_stock_price
from .commands.avatar import get_user_avatar
from .commands.storage import fetch_image_from_storage
from .commands.reddit import random_subreddit_image


class Bot(ch.RoomManager):
    """Main bot class."""

    def onInit(self):
        """Initialize bot."""
        self.setNameColor("000000")
        self.setFontColor("000000")
        self.setFontFace("Arial")
        self.setFontSize(11)

    def chat(self, row, room):
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
            print('goal command')
        if type == 'stock':
            response = get_stock_price(message)
        if type == 'avi':
            response = get_user_avatar(message)
        if type == 'storage':
            response = fetch_image_from_storage(message)
        if type == 'reddit':
            response = random_subreddit_image(message)
        room.message(response)

    def onMessage(self, room, user, message):
        """Boilerplate function trigger on message."""
        print("[{0}] {1}: {2}".format(room.name,
                                      user.name.title(),
                                      message.body))

        # cmd = message.body.replace(" ", '')
        cmd = message.body.lower()
        # Trigger if chat message is a command
        try:
            if cmd[0] == "!":
                cmd = cmd[1::].lower()
                response = db.cm(cmd)
                self.chat(response, room)
        except KeyError:
            pass
