"""Core bot logic."""
import sys
from loguru import logger
from .ch import RoomManager
from .logic import (basic_message,
                    get_crypto_price,
                    random_image,
                    stock_price_chart,
                    fetch_image_from_gcs,
                    giphy_image_search,
                    subreddit_image,
                    weather_by_city,
                    urban_dictionary,
                    wiki_summary,
                    find_imdb_movie)

logger.add(
    sys.stderr,
    format="<green>{time:MM-DD HH:mm A}</green> <white>{message}</white>",
    catch=True,
    colorize=True,
)


class Bot(RoomManager):

    def on_init(self):
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

    def create_message(self, cmd_type, content, command=None, args=None):
        response = None
        if cmd_type == 'basic':
            response = basic_message(content)
        elif cmd_type == 'crypto':
            response = get_crypto_price(command, content)
        elif cmd_type == 'random':
            response = random_image(content)
        elif cmd_type == 'stock' and args:
            response = stock_price_chart(args)
        elif cmd_type == 'storage':
            response = fetch_image_from_gcs(content)
        elif cmd_type == 'giphy':
            response = giphy_image_search(content)
        # elif cmd_type == 'urban' and args:
            # response = urban_dictionary(args)
        # elif cmd_type == 'nba' and args:
            # response = nba_team_score(args)
        elif cmd_type == 'reddit':
            response = subreddit_image(content)
        elif cmd_type == 'weather' and args:
            response = weather_by_city(args, self.weather)
        elif cmd_type == 'wiki' and args:
            response = wiki_summary(args)
        elif cmd_type == 'imdb' and args:
            response = find_imdb_movie(args)
        return response

    @logger.catch
    def on_message(self, room, user, message):
        """Boilerplate function trigger on message."""
        logger.info("[{0}] {1} ({2}): {3}".format(room.name,
                                                  user.name.title(),
                                                  message.ip,
                                                  message.body))
        user_msg = message.body.lower()
        if user_msg[0] == "!":
            self.command_response(user_msg, room)  # Trigger if message is a command
        elif user_msg == 'bro?':
            self.bot_status_check(room)
        elif user_msg.endswith('only on aclee'):
            self._chat(room, '™')
        elif user_msg.lower() == 'tm':
            self.replace_word(room, message)
        # elif re.search('bl(\S+)b', user_msg) and 'south' not in user_msg and 'http' not in user_msg and 'blow' not in user_msg:
           # self.banned_word(room, message, user)

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
        command = self.commands.find_row(cmd)
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
