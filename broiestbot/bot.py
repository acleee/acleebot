"""Chatango bot."""
from broiestbot.logging import LOGGER
from .ch import RoomManager
from .commands import (
    basic_message,
    get_crypto,
    random_image,
    get_stock,
    fetch_image_from_gcs,
    giphy_image_search,
    subreddit_image,
    weather_by_city,
    wiki_summary,
    find_imdb_movie,
    get_redgifs_gif,
    get_urban_definition,
    blaze_time_remaining
)


class Bot(RoomManager):
    """Chatango bot."""

    def on_init(self):
        """Initialize bot."""
        self.setNameColor("000000")
        self.setFontColor("000000")
        self.setFontFace("Arial")
        self.setFontSize(11)

    @staticmethod
    def _chat(room, message):
        """Construct a response to a valid command."""
        room.message(message)

    def create_message(self, cmd_type, content, command=None, args=None):
        """Router to resolve bot response."""
        response = None
        if cmd_type == 'basic':
            response = basic_message(content)
        elif cmd_type == 'crypto' and not args:
            response = get_crypto(command)
        elif cmd_type == 'random':
            response = random_image(content)
        elif cmd_type == 'stock' and args:
            response = get_stock(args)
        elif cmd_type == 'storage':
            response = fetch_image_from_gcs(content)
        elif cmd_type == 'giphy':
            response = giphy_image_search(content)
        elif cmd_type == 'reddit':
            response = subreddit_image(content)
        elif cmd_type == 'weather' and args:
            response = weather_by_city(args, self.weather)
        elif cmd_type == 'wiki' and args:
            response = wiki_summary(args)
        elif cmd_type == 'imdb' and args:
            response = find_imdb_movie(args)
        elif cmd_type == 'nsfw' and args is None:
            response = get_redgifs_gif('lesbians', after_dark_only=False)
        elif cmd_type == 'nsfw' and args:
            response = get_redgifs_gif(args, after_dark_only=True)
        elif cmd_type == 'urban' and args:
            response = get_urban_definition(args)
        elif cmd_type == '420' and args is None:
            response = blaze_time_remaining()
        if response:
            return response
        LOGGER.debug(f'No response for command {command} with args {args}')

    def on_message(self, room, user, message):
        """Boilerplate function trigger on message."""
        LOGGER.info(f"[{room.name}] [{user.name.title()}] [{message.ip}]: {message.body}")
        chat_message = message.body.lower()
        if chat_message[0] == "!":
            self.parse_command(chat_message, room, user)  # Trigger if command
        elif chat_message == 'bro?':
            self.bot_status_check(room)
        elif chat_message.endswith('only on aclee'):
            self._chat(room, '™')
        elif chat_message.lower() == 'tm':
            self.replace_word(room, message)
        # elif re.search('bl(\S+)b', user_msg) and 'south' not in user_msg and 'http' not in user_msg and 'blow' not in user_msg:
           # self.banned_word(room, message, user)

    def parse_command(self, user_msg, room, user):
        """Respond to command."""
        user_msg = user_msg[1::].lower()
        args = None
        if ' ' not in user_msg:
            cmd = user_msg
        else:
            cmd = user_msg.split(' ', 1)[0]
            args = user_msg.split(' ', 1)[1]
        command = self.commands.find_row(cmd)
        if command is not None:
            message = self.create_message(
                command['type'],
                command['response'],
                command=cmd,
                args=args
            )
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
