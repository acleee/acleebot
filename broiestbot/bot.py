"""Chatango bot."""
import re
from typing import Optional, Tuple

from emoji import emojize

from broiestbot.commands import (
    basic_message,
    blaze_time_remaining,
    bund_standings,
    covid_cases_usa,
    create_instagram_preview,
    epl_golden_boot,
    epl_standings,
    fetch_fox_fixtures,
    fetch_image_from_gcs,
    find_imdb_movie,
    footy_live_fixtures,
    footy_predicts_today,
    footy_upcoming_fixtures,
    get_crypto,
    get_english_translation,
    get_redgifs_gif,
    get_song_lyrics,
    get_stock,
    get_urban_definition,
    giphy_image_search,
    liga_standings,
    random_image,
    send_text_message,
    weather_by_location,
    wiki_summary,
)
from chatango.ch import Message, Room, RoomManager, User
from clients import db
from config import CHATANGO_BLACKLISTED_USERS
from logger import LOGGER


class Bot(RoomManager):
    """Chatango bot."""

    def on_init(self):
        """Initialize bot."""
        self.set_name_color("000000")
        self.set_font_color("000000")
        self.set_font_face("Arial")
        self.set_font_size(11)

    @staticmethod
    def create_message(
        cmd_type,
        content,
        command: Optional[str] = None,
        args: Optional[str] = None,
        room: Optional[Room] = None,
        user: Optional[User] = None,
    ) -> Optional[str]:
        """
        Construct a message response based on command type and arguments.

        :param str cmd_type: `Type` of command triggered by a user.
        :param str content: Content to be used in response.
        :param Optional[str] command: Name of command triggered by user.
        :param Optional[str] args: Additional arguments passed with user command.
        :param Optional[Room] room: Chatango room.
        :param Optional[User] user: User who triggered command.

        :returns: Optional[str]
        """
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
        elif cmd_type == "weather" and args:
            return weather_by_location(args, room.room_name, user.name.title().lower())
        elif cmd_type == "wiki" and args:
            return wiki_summary(args)
        elif cmd_type == "imdb" and args:
            return find_imdb_movie(args)
        elif cmd_type == "nsfw" and args is None:
            return get_redgifs_gif(
                "lesbians", user.name.title().lower(), after_dark_only=False
            )
        elif cmd_type == "nsfw" and args:
            return get_redgifs_gif(
                args, user.name.title().lower(), after_dark_only=True
            )
        elif cmd_type == "urban" and args:
            return get_urban_definition(args)
        elif cmd_type == "420" and args is None:
            return blaze_time_remaining()
        elif cmd_type == "sms" and args and user:
            return send_text_message(args, user.name.title())
        elif cmd_type == "epltable":
            return epl_standings(content)
        elif cmd_type == "ligatable":
            return liga_standings(content)
        elif cmd_type == "bundtable":
            return bund_standings(content)
        elif cmd_type == "fixtures":
            return footy_upcoming_fixtures(
                room.room_name.lower(), user.name.title().lower()
            )
        elif cmd_type == "livefixtures":
            return footy_live_fixtures(
                room.room_name.lower(), user.name.title().lower()
            )
        elif cmd_type == "goldenboot":
            return epl_golden_boot()
        elif cmd_type == "eplpredicts":
            return footy_predicts_today(
                room.room_name.lower(), user.name.title().lower()
            )
        elif cmd_type == "foxtures":
            return fetch_fox_fixtures(room.room_name.lower(), user.name.title().lower())
        elif cmd_type == "covid":
            return covid_cases_usa()
        elif cmd_type == "lyrics" and args:
            return get_song_lyrics(args)
        elif cmd_type == "entranslation" and args:
            return get_english_translation(command, args)
        LOGGER.warning(f"No response for command `{command}` {args}")
        return None

    def on_message(self, room: Room, user: User, message: Message) -> None:
        """
        Boilerplate function trigger on message.

        :param Room room: Chatango room.
        :param User user: User responsible for triggering command.
        :param Message message: Raw chat message submitted by a user.

        :returns: None
        """
        chat_message = message.body.lower()
        self.check_blacklisted_users(room, user, message)
        if re.match(r"^!!.+", chat_message):
            return self._giphy_fallback(chat_message[2::], room)
        elif re.match(r"^!.+", chat_message):
            cmd, args = self._parse_command(chat_message[1::])
            self._get_response(chat_message, cmd, args, room, user=user)
        elif chat_message == "bro?":
            self._bot_status_check(room)
        elif (
            "@broiestbro" in chat_message.lower() and "*waves*" in chat_message.lower()
        ):
            self._wave_back(room, user)
        elif chat_message.replace("!", "").strip() == "no u":
            self._ban_word(room, message, user, silent=True)
        elif (
            "petition" in chat_message
            and "competition" not in chat_message
            and user.name.title() != "Broiestbro"
        ):
            room.message(
                "SIGN THE PETITION: \
                                https://www.change.org/p/nhl-exclude-penguins-from-bird-team-classification \
                                https://i.imgur.com/nYQy0GR.jpg",
            )
        elif chat_message.endswith("only on aclee"):
            room.message("™")
        elif chat_message.lower() == "tm":
            self._trademark(room, message)
        # elif re.search(r"instagram.com/p/[a-zA-Z0-9_-]+", message.body):
        # self._create_link_preview(room, message.body)
        LOGGER.info(f"[{room.room_name}] [{user.name}] [{message.ip}]: {message.body}")

    @staticmethod
    def _parse_command(user_msg: str) -> Tuple[str, Optional[str]]:
        """
        Parse user message into command & arguments.

        :param str user_msg: Raw chat message submitted by a user.

        :returns: Tuple[str, Optional[str]]
        """
        user_msg = user_msg.lower().strip()
        if " " in user_msg:
            cmd = user_msg.split(" ", 1)[0]
            args = user_msg.split(" ", 1)[1]
            LOGGER.trace(f"Command `{cmd}` found with args `{args}`.")
            return cmd, args
        LOGGER.trace(f"Command `{user_msg}` found with no args.")
        return user_msg, None

    def _get_response(
        self,
        chat_message: str,
        cmd: str,
        args: Optional[str],
        room: Room,
        user: Optional[User] = None,
    ) -> Optional[str]:
        """
        Fetch response from database to send to chat.

        :param str chat_message: Raw message sent by user.
        :param str cmd: Command triggered by a user.
        :param Optional[str] args: Additional arguments passed with user command.
        :param Room room: Chatango room.
        :param Optional[User] user: User responsible for triggering command.

        :returns: Optional[str]
        """
        if cmd == "tune":  # Avoid clashes with Acleebot
            return None
        command = db.fetch_command_response(cmd)
        if command is not None:
            response = self.create_message(
                command["type"],
                command["response"],
                command=cmd,
                args=args,
                room=room,
                user=user,
            )
            room.message(response)
        else:
            self._giphy_fallback(chat_message, room)

    @staticmethod
    def _create_link_preview(room: Room, url: str) -> None:
        """
        Generate link preview for Instagram post URL.

        :param room: Chatango room.
        :type room: Room
        :param url: URL of an Instagram post.
        :type url: str
        :returns: None
        """
        preview = create_instagram_preview(url)
        room.message(preview)

    @staticmethod
    def _bot_status_check(room: Room) -> None:
        """
        Check bot status.

        :param room: Chatango room.
        :type room: Room
        :returns: None
        """
        room.message("hellouughhgughhg?")

    @staticmethod
    def _wave_back(room: Room, user: User) -> None:
        """
        Wave back at user.

        :param Room room: Chatango room.
        :param User user: Chatango user who waved.

        :returns: None
        """
        if user.name == "broiestbro":
            room.message(
                f"lol stop talking to urself and get some friends u fuckin loser jfc kys @broiestbro"
            )
        else:
            room.message(f"@{user.name} *waves*")

    @staticmethod
    def _giphy_fallback(message: str, room: Room):
        """
        Default to Giphy for non-existent commands.

        :param str message: Command triggered by a user.
        :param Room room: Chatango room.

        :returns: Optional[str]
        """
        query = message.replace("!", "").lower().strip()
        if len(query) > 1:
            response = giphy_image_search(query)
            room.message(response)

    @staticmethod
    def _ban_word(room: Room, message: Message, user: User, silent=False) -> None:
        """
        Remove banned word and warn offending user.

        :param Room room: Chatango room.
        :param Message message: Message sent by user.
        :param User user: User responsible for triggering command.
        :param bool silent: Whether or not offending user should be warned.

        :returns: None
        """
        message.delete()
        if silent is False:
            room.message(f"DO NOT SAY THAT WORD @{user.name.upper()} :@")

    @staticmethod
    def _trademark(room: Room, message: Message) -> None:
        """
        Trademark symbol helper.

        :param Room room: Chatango room.
        :param Message message: User submitted `tm` to be replaced.

        :returns: None
        """
        message.delete()
        room.message("™")

    @staticmethod
    def check_blacklisted_users(room: Room, user: User, message: Message) -> None:
        """
        Ban and delete chat history of blacklisted user.

        :param Room room: Chatango room.
        :param User user: Chatango user to validate against blacklist.
        :param Message message: User submitted message.

        :returns: None
        """
        if user.name.title().lower() in CHATANGO_BLACKLISTED_USERS:
            room.ban(message)
            reply = emojize(
                f":wave: @{user.name.title()} lmao pz fgt have fun being banned forever :wave:",
                use_aliases=True,
            )
            room.message(reply)
