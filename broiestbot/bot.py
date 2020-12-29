"""Chatango bot."""
import re

from chatango.ch import RoomManager
from logger import LOGGER

from .commands import (
    basic_message,
    blaze_time_remaining,
    create_instagram_preview,
    fetch_image_from_gcs,
    find_imdb_movie,
    get_crypto,
    get_redgifs_gif,
    get_stock,
    get_urban_definition,
    giphy_image_search,
    random_image,
    subreddit_image,
    weather_by_city,
    wiki_summary,
)


class Bot(RoomManager):
    """Chatango bot."""

    def on_init(self):
        """Initialize bot."""
        self.set_name_color("000000")
        self.set_font_color("000000")
        self.set_font_face("Arial")
        self.set_font_size(11)

    @staticmethod
    def _chat(room, message):
        """Construct a response to a valid command."""
        room.message(message)

    def create_message(self, cmd_type, content, command=None, args=None):
        """Router to resolve bot response."""
        response = None
        if cmd_type == "basic":
            response = basic_message(content)
        elif cmd_type == "crypto" and not args:
            response = get_crypto(command)
        elif cmd_type == "random":
            response = random_image(content)
        elif cmd_type == "stock" and args:
            response = get_stock(args)
        elif cmd_type == "storage":
            response = fetch_image_from_gcs(content)
        elif cmd_type == "giphy":
            response = giphy_image_search(content)
        elif cmd_type == "reddit":
            response = subreddit_image(content)
        elif cmd_type == "weather" and args:
            response = weather_by_city(args, self.weather)
        elif cmd_type == "wiki" and args:
            response = wiki_summary(args)
        elif cmd_type == "imdb" and args:
            response = find_imdb_movie(args)
        elif cmd_type == "nsfw" and args is None:
            response = get_redgifs_gif("lesbians", after_dark_only=False)
        elif cmd_type == "nsfw" and args:
            response = get_redgifs_gif(args, after_dark_only=True)
        elif cmd_type == "urban" and args:
            response = get_urban_definition(args)
        elif cmd_type == "420" and args is None:
            response = blaze_time_remaining()
        if response:
            return response
        LOGGER.warning(f"No response for command `{command}` {args}")

    def on_message(self, room, user, message):
        """Boilerplate function trigger on message."""
        chat_message = message.body.lower()
        if chat_message[0] == "!":
            self.parse_command(chat_message, room)  # Trigger if command
        elif chat_message == "bro?":
            self.bot_status_check(room)
        elif "petition" in chat_message and user.name.title() != "Broiestbro":
            self._chat(
                room,
                "SIGN THE PETITION: \
                                https://www.change.org/p/nhl-exclude-penguins-from-bird-team-classification \
                                https://i.imgur.com/nYQy0GR.jpg",
            )
        elif chat_message.endswith("only on aclee"):
            self._chat(room, "™")
        elif chat_message.lower() == "tm":
            self.trademark(room, message)
        elif chat_message == "https://lmao.love/truth":
            self.ban_word(room, message, user, silent=True)
        elif re.search(r"instagram.com/p/[a-zA-Z0-9_-]+", message.body):
            self.link_preview(room, message.body)
        LOGGER.info(f"[{room.name}] [{user.name}] [{message.ip}]: {message.body}")
        # elif re.search('bl(\S+)b', user_msg) and 'south' not in user_msg and 'http' not in user_msg and 'blow' not in user_msg:
        # self.banned_word(room, message, user)

    def parse_command(self, user_msg, room):
        """Respond to command."""
        user_msg = user_msg[1::].lower()
        args = None
        if " " not in user_msg:
            cmd = user_msg
        else:
            cmd = user_msg.split(" ", 1)[0]
            args = user_msg.split(" ", 1)[1]
        command = self.commands.find_row("command", cmd)
        if command is not None:
            message = self.create_message(
                command["type"], command["response"], command=cmd, args=args
            )
            if message:
                self._chat(room, message)
        else:
            self.giphy_fallback(user_msg, room)

    @staticmethod
    def link_preview(room, message):
        preview = create_instagram_preview(message)
        room.message(preview)

    @staticmethod
    def bot_status_check(room):
        """Check bot status."""
        room.message("hellouughhgughhg?")

    @staticmethod
    def giphy_fallback(cmd, room):
        """Default to Giphy for non-existent commands."""
        cmd = cmd.replace("!", "")
        if len(cmd) > 1:
            response = giphy_image_search(cmd)
            room.message(response)

    @staticmethod
    def ban_word(room, message, user, silent=False):
        """Remove banned words."""
        message.delete()
        if silent is False:
            room.message(f"DO NOT SAY THAT WORD @{user.name.upper()} :@")

    @staticmethod
    def trademark(room, message):
        """Trademark symbol helper."""
        message.delete()
        room.message("™")
