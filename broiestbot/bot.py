"""Chatango bot."""
import re
from typing import Optional, Tuple

from database import session
from database.models import Command, Phrase
from emoji import emojize

from broiestbot.commands import (
    all_leagues_golden_boot,
    basic_message,
    blaze_time_remaining,
    bund_standings,
    covid_cases_usa,
    epl_golden_boot,
    epl_standings,
    extract_url,
    fetch_fox_fixtures,
    fetch_image_from_gcs,
    find_imdb_movie,
    footy_all_upcoming_fixtures,
    footy_live_fixtures,
    footy_predicts_today,
    footy_todays_upcoming_fixtures,
    footy_upcoming_fixtures,
    get_all_live_twitch_streams,
    get_crypto,
    get_current_show,
    get_english_definition,
    get_english_translation,
    get_footy_odds,
    get_live_nfl_games,
    get_redgifs_gif,
    get_song_lyrics,
    get_stock,
    get_summer_olympic_medals,
    get_top_crypto,
    get_urban_definition,
    get_winter_olympic_medals,
    giphy_image_search,
    liga_standings,
    random_image,
    send_text_message,
    time_until_wayne,
    tuner,
    weather_by_location,
    wiki_summary,
)
from chatango.ch import Message, Room, RoomManager, User
from config import CHATANGO_BLACKLISTED_USERS, CHATANGO_EGGSER_IP
from logger import LOGGER

from .data import persist_chat_data, persist_user_data


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
        user_name: Optional[str] = None,
    ) -> Optional[str]:
        """
        Construct a message response based on command type and arguments.

        :param str cmd_type: `Type` of command triggered by a user.
        :param str content: Content to be used in response.
        :param Optional[str] command: Name of command triggered by user.
        :param Optional[str] args: Additional arguments passed with user command.
        :param Optional[Room] room: Current Chatango room object.
        :param Optional[str] user_name: User who triggered command.

        :returns: Optional[str]
        """
        if cmd_type == "basic":
            return basic_message(content)
        elif cmd_type == "random":
            return random_image(content)
        elif cmd_type == "stock" and args:
            return get_stock(args)
        elif cmd_type == "storage":
            return fetch_image_from_gcs(content)
        elif cmd_type == "crypto":
            return get_crypto(content)
        elif cmd_type == "giphy":
            return giphy_image_search(content)
        elif cmd_type == "weather" and args:
            return weather_by_location(args, room.room_name, user_name)
        elif cmd_type == "wiki" and args:
            return wiki_summary(args)
        elif cmd_type == "imdb" and args:
            return find_imdb_movie(args)
        elif cmd_type == "lesbians":
            return get_redgifs_gif("lesbians", user_name)
        elif cmd_type == "nsfw" and args:
            return get_redgifs_gif(args, user_name, after_dark_only=True)
        elif cmd_type == "urban" and args:
            return get_urban_definition(args)
        elif cmd_type == "420" and args is None:
            return blaze_time_remaining()
        elif cmd_type == "sms" and args and user_name:
            return send_text_message(args, user_name)
        elif cmd_type == "epltable":
            return epl_standings(content)
        elif cmd_type == "ligatable":
            return liga_standings(content)
        elif cmd_type == "bundtable":
            return bund_standings(content)
        elif cmd_type == "fixtures":
            return footy_upcoming_fixtures(room.room_name.lower(), user_name)
        elif cmd_type == "allfixtures":
            return footy_all_upcoming_fixtures(room.room_name.lower(), user_name)
        elif cmd_type == "livefixtures":
            return footy_live_fixtures(room.room_name.lower(), user_name)
        elif cmd_type == "livefixtureswithsubs":
            return footy_live_fixtures(room.room_name.lower(), user_name, subs=True)
        elif cmd_type == "todayfixtures":
            return footy_todays_upcoming_fixtures(room.room_name.lower(), user_name)
        elif cmd_type == "goldenboot":
            return epl_golden_boot()
        elif cmd_type == "goldenshoe":
            return all_leagues_golden_boot()
        elif cmd_type == "eplpredicts":
            return footy_predicts_today(room.room_name.lower(), user_name)
        elif cmd_type == "foxtures":
            return fetch_fox_fixtures(room.room_name.lower(), user_name)
        elif cmd_type == "covid":
            return covid_cases_usa()
        elif cmd_type == "lyrics" and args:
            return get_song_lyrics(args)
        elif cmd_type == "entranslation" and args:
            return get_english_translation(command, args)
        elif cmd_type == "olympics":
            return get_summer_olympic_medals()
        elif cmd_type in ("wolympics", "winterolympics"):
            return get_winter_olympic_medals()
        elif cmd_type == "eplodds":
            return get_footy_odds()
        elif cmd_type == "twitch":
            return get_all_live_twitch_streams()
        elif cmd_type == "livenfl":
            return get_live_nfl_games()
        elif cmd_type == "topcrypto":
            return get_top_crypto()
        elif cmd_type == "define" and args:
            return get_english_definition(args)
        elif cmd_type == "tune" and args:
            return tuner(args, user_name, room.user.name.lower())
        elif cmd_type == "wayne":
            return time_until_wayne()
        elif cmd_type == "np":
            return get_current_show(True, room.user.name.lower())
        elif cmd_type == "reserved":
            pass
        # elif cmd_type == "youtube" and args:
        # return search_youtube_for_video(args)
        LOGGER.warning(f"No response for command `{command}` {args}")
        return emojize(f":warning: idk wtf u did but bot is ded now, thanks @{user_name} :warning:")

    def on_message(self, room: Room, user: User, message: Message) -> None:
        """
        Triggers upon every chat message to parse commands, validate users, and save chat logs.

        :param Room room: Current Chatango room object.
        :param User user: User responsible for triggering command.
        :param Message message: Raw chat message submitted by a user.

        :returns: None
        """
        chat_message = message.body.lower()
        user_name = user.name.lower()
        room_name = room.room_name.lower()
        bot_username = room.user.name.lower()
        self._check_blacklisted_users(room, user_name, message)
        self._log_message(room, user, message)
        persist_user_data(room_name, user, message, bot_username)
        persist_chat_data(user_name, room_name, chat_message, bot_username)
        if chat_message.startswith("!"):
            self._process_command(chat_message, room, user_name)
        # elif message.body.startswith("http"):
        # self._create_link_preview(room, message.body)
        # elif re.match(r"bl\/S+b", chat_message) and "south" not in chat_message:
            # self._ban_word(room, message, user_name, silent=False)
        else:
            self._process_phrase(chat_message, room, user_name, message, bot_username)

    @staticmethod
    def _log_message(room: Room, user: User, message: Message):
        """
        Log chat message.

        :param Room room: Current Chatango room object.
        :param User user: User responsible for triggering command.
        :param Message message: Raw chat message submitted by a user.

        :returns: None
        """
        if bool(message.ip) is True and message.body is not None:
            LOGGER.info(f"[{room.room_name}] [{user.name}] [{message.ip}]: {message.body}")
        else:
            LOGGER.info(f"[{room.room_name}] [{user.name}] [no IP address]: {message.body}")

    def _process_command(self, chat_message: str, room: Room, user_name: str) -> None:
        """
        Determines if message is a bot command.

        :param str chat_message: Raw message sent by user.
        :param Room room: Chatango room object.
        :param str user_name: User responsible for triggering command.

        :returns: None
        """
        if re.match(r"^!!.+", chat_message):
            return self._giphy_fallback(chat_message[2::], room)
        elif re.match(r"^!ein+$", chat_message):
            return self._get_response("!ein", room, user_name)
        elif re.match(r"^!\S+", chat_message):
            return self._get_response(chat_message, room, user_name)
        # elif re.search(r"instagram.com/p/[a-zA-Z0-9_-]+", message.body):

    def _process_phrase(
        self, chat_message: str, room: Room, user_name: str, message: Message, bot_username: str
    ) -> None:
        """
        Search database for non-command phrases which elicit a response.

        :param str chat_message: A non-command chat which may prompt a response.
        :param Room room: Current chatango room object.
        :param str user_name: User responsible for triggering command.
        :param Message message: Chatango message object to be parsed.
        :param str bot_username: Username of the currently-running bot.

        :returns: None
        """
        if f"@{bot_username}" in chat_message and "*waves*" in chat_message:
            self._wave_back(room, user_name, bot_username)
        elif chat_message == "no u":
            self._ban_word(room, message, user_name, silent=True)
        elif (
            "petition" in chat_message
            and "competition" not in chat_message
            and user_name != bot_username
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
        else:
            fetched_phrase = (
                session.query(Phrase).filter(Phrase.phrase == chat_message).one_or_none()
            )
            if fetched_phrase is not None:
                room.message(fetched_phrase.response)

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
            return cmd, args
        return user_msg, None

    def _get_response(self, chat_message: str, room: Room, user_name: str):
        """
        Fetch response from database to send to chat.

        :param str chat_message: Raw message sent by user.
        :param Room room: Current Chatango room object.
        :param str user_name: User responsible for triggering command.
        """
        cmd, args = self._parse_command(chat_message[1::])
        command = session.query(Command).filter(Command.command == cmd).first()
        if command is not None and command.type not in ("reserved", "reddit"):
            response = self.create_message(
                command.type,
                command.response,
                command=cmd,
                args=args,
                room=room,
                user_name=user_name,
            )
            room.message(response, html=True)
        # elif command.type == "reserved":
        # pass
        else:
            self._giphy_fallback(chat_message, room)

    @staticmethod
    def _create_link_preview(room: Room, chat_message: str) -> None:
        """
        Generate link preview for URL.

        :param Room room: Current Chatango room object.
        :param str chat_message: URL of an Instagram post.

        :returns: None
        """
        if (
            ".jpg" not in chat_message
            and ".png" not in chat_message
            and ".gif" not in chat_message
            and ".jpeg" not in chat_message
            and ".mp4" not in chat_message
            and ".JPG" not in chat_message
            and ".PNG" not in chat_message
            and ".GIF" not in chat_message
            and ".JPEG" not in chat_message
            and ".MP4" not in chat_message
            and "twitter" not in chat_message
            and "youtube" not in chat_message
        ):
            link_preview = extract_url(chat_message)
            if link_preview:
                room.message(link_preview, html=True)

    @staticmethod
    def _wave_back(room: Room, user_name: str, bot_username) -> None:
        """
        Wave back at user.

        :param Room room: Current Chatango room object.
        :param str user_name: Username of Chatango user who waved.

        :returns: None
        """
        if user_name == bot_username:
            room.message(
                f"stop talking to urself and get some friends u fuckin loser jfc kys @{bot_username}"
            )
        else:
            room.message(f"@{user_name} *waves*")

    @staticmethod
    def _giphy_fallback(message: str, room: Room) -> None:
        """
        Default to Giphy for non-existent commands.

        :param str message: Command triggered by a user.
        :param Room room: Current Chatango room object.

        :returns: None
        """
        query = message.replace("!", "").lower().strip()
        if len(query) > 1:
            response = giphy_image_search(query)
            room.message(response)

    @staticmethod
    def _ban_word(room: Room, message: Message, user_name: str, silent=False) -> None:
        """
        Remove banned word and warn offending user.

        :param Room room: Current Chatango room object.
        :param Message message: Message sent by user.
        :param str user_name: User responsible for triggering command.
        :param bool silent: Whether offending user should be warned.

        :returns: None
        """
        message.delete()
        if silent is not True:
            room.message(f"DO NOT SAY THAT WORD @{user_name.upper()} :@")

    @staticmethod
    def _trademark(room: Room, message: Message) -> None:
        """
        Trademark symbol helper.

        :param Room room: Current Chatango room object.
        :param Message message: User submitted `tm` to be replaced.

        :returns: None
        """
        message.delete()
        room.message("™")

    @staticmethod
    def _check_blacklisted_users(room: Room, user_name: str, message: Message) -> None:
        """
        Ban and delete chat history of blacklisted user.

        :param Room room: Chatango room name.
        :param str user_name: Chatango username to validate against blacklist.
        :param Message message: User submitted message.

        :returns: None
        """
        if user_name in CHATANGO_BLACKLISTED_USERS:
            reply = emojize(
                f":wave: @{user_name} lmao pz fgt have fun being banned forever :wave:",
                use_aliases=True,
            )
            room.message(reply)
            room.ban_user(message.user)
        elif message.ip and CHATANGO_EGGSER_IP in message.ip:
            room.ban_user(message.user)
