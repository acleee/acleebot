"""Chatango bot."""
import re
from typing import Optional, Tuple

from chatango.ch import Message, Room, RoomManager
from logger import LOGGER

from .commands import (
    basic_message,
    blaze_time_remaining,
    create_instagram_preview,
    epl_standings,
    fetch_image_from_gcs,
    find_imdb_movie,
    get_crypto,
    get_redgifs_gif,
    get_stock,
    get_urban_definition,
    giphy_image_search,
    random_image,
    send_text_message,
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

    def create_message(
        self, cmd_type, content, command=None, args=None, room=None, user=None
    ):
        """Router to resolve bot response."""
        if cmd_type == "basic":
            return basic_message(content)
        elif cmd_type == "crypto" and not args:
            return get_crypto(command)
        elif cmd_type == "random":
            return random_image(content)
        elif cmd_type == "stock" and args:
            return get_stock(args)
        elif cmd_type == "storage":
            return fetch_image_from_gcs(content)
        elif cmd_type == "giphy":
            return giphy_image_search(content)
        elif cmd_type == "reddit":
            return subreddit_image(content)
        elif cmd_type == "weather" and args:
            return weather_by_city(args, self.weather, room.name)
        elif cmd_type == "wiki" and args:
            return wiki_summary(args)
        elif cmd_type == "imdb" and args:
            return find_imdb_movie(args)
        elif cmd_type == "nsfw" and args is None:
            return get_redgifs_gif("lesbians", after_dark_only=False)
        elif cmd_type == "nsfw" and args:
            return get_redgifs_gif(args, after_dark_only=True)
        elif cmd_type == "urban" and args:
            return get_urban_definition(args)
        elif cmd_type == "420" and args is None:
            return blaze_time_remaining()
        elif cmd_type == "sms" and args and user:
            return send_text_message(args, user.name.title())
        elif cmd_type == "epltable":
            return epl_standings()
        LOGGER.warning(f"No response for command `{command}` {args}")

    def on_message(self, room: Room, user, message: Message):
        """Boilerplate function trigger on message."""
        chat_message = message.body.lower()
        if chat_message[0] == "!":
            cmd, args = self.parse_command(chat_message)
            sent = self.send_message(cmd, args, room, user=user)
            if sent is False:
                self.giphy_fallback(chat_message, room)
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

    @staticmethod
    def parse_command(user_msg) -> Tuple[str, Optional[str]]:
        """Respond to command."""
        user_msg = user_msg[1::].lower()
        cmd = user_msg
        args = None
        if " " in user_msg:
            cmd = user_msg.split(" ", 1)[0]
            args = user_msg.split(" ", 1)[1]
        return cmd, args

    def send_message(self, cmd: str, args: Optional[str], room: Room, user=None):
        """Send response to chat."""
        command = self.commands.find_row("command", cmd)
        if command is not None:
            message = self.create_message(
                command["type"],
                command["response"],
                command=cmd,
                args=args,
                room=room,
                user=user,
            )
            if message:
                self._chat(room, message)
                return True
        return False

    @staticmethod
    def link_preview(room: Room, message):
        preview = create_instagram_preview(message)
        room.message(preview)

    @staticmethod
    def bot_status_check(room: Room):
        """Check bot status."""
        room.message("hellouughhgughhg?")

    @staticmethod
    def giphy_fallback(cmd: str, room: Room):
        """Default to Giphy for non-existent commands."""
        cmd = cmd.replace("!", "").lower()
        if len(cmd) > 1:
            response = giphy_image_search(cmd)
            if response is not None:
                room.message(response)

    @staticmethod
    def ban_word(room: Room, message, user, silent=False):
        """Remove banned words."""
        message.delete()
        if silent is False:
            room.message(f"DO NOT SAY THAT WORD @{user.name.upper()} :@")

    @staticmethod
    def trademark(room: Room, message):
        """Trademark symbol helper."""
        message.delete()
        room.message("™")
