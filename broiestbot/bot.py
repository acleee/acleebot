"""Chatango bot."""
import re
from typing import Optional, Tuple

from emoji import emojize
from ipdata.ipdata import IncompatibleParameters

from broiestbot.commands import (
    all_leagues_golden_boot,
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
    footy_all_upcoming_fixtures,
    footy_live_fixtures,
    footy_predicts_today,
    footy_todays_upcoming_fixtures,
    footy_upcoming_fixtures,
    get_all_live_twitch_streams,
    get_crypto,
    get_english_definition,
    get_english_translation,
    get_footy_odds,
    get_live_nfl_games,
    get_olympic_medals_per_nation,
    get_redgifs_gif,
    get_song_lyrics,
    get_stock,
    get_top_crypto,
    get_urban_definition,
    giphy_image_search,
    liga_standings,
    random_image,
    send_text_message,
    tuner,
    weather_by_location,
    wiki_summary,
)
from chatango.ch import Message, Room, RoomManager, User
from clients import geo
from config import CHATANGO_BLACKLISTED_USERS
from database import session
from database.models import Chat, ChatangoUser, Command
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
        user_name: Optional[str] = None,
    ) -> Optional[str]:
        """
        Construct a message response based on command type and arguments.

        :param str cmd_type: `Type` of command triggered by a user.
        :param str content: Content to be used in response.
        :param Optional[str] command: Name of command triggered by user.
        :param Optional[str] args: Additional arguments passed with user command.
        :param Optional[Room] room: Chatango room.
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
            return get_olympic_medals_per_nation()
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
            return tuner(args, user_name)
        # elif cmd_type == "youtube" and args:
        # return search_youtube_for_video(args)
        LOGGER.warning(f"No response for command `{command}` {args}")
        return None

    def on_message(self, room: Room, user: User, message: Message) -> None:
        """
        Triggers upon every chat message to parse commands, validate users, and save chat logs.

        :param Room room: Chatango room.
        :param User user: User responsible for triggering command.
        :param Message message: Raw chat message submitted by a user.

        :returns: None
        """
        chat_message = message.body.lower()
        user_name = user.name.title().lower()
        room_name = room.room_name.lower()
        self._check_blacklisted_users(room, user_name, message)
        self._get_user_data(room_name, user, message)
        self._process_command(chat_message, room, user_name, message)
        session.add(Chat(username=user_name, room=room_name, message=chat_message))

    def _process_command(self, chat_message: str, room: Room, user_name: str, message: Message) -> None:
        """Determines if message is a bot command."""
        if re.match(r"^!!.+", chat_message):
            return self._giphy_fallback(chat_message[2::], room)
        elif re.match(r"^!ein+", chat_message):
            return self._get_response("!ein", room, user_name)
        elif re.match(r"^!.+", chat_message):
            return self._get_response(chat_message, room, user_name)
        elif chat_message == "bro?":
            self._bot_status_check(room)
        elif "@broiestbro" in chat_message.lower() and "*waves*" in chat_message.lower():
            self._wave_back(room, user_name)
        elif chat_message.replace("!", "").strip() == "no u":
            self._ban_word(room, message, user_name, silent=True)
        elif "petition" in chat_message and "competition" not in chat_message and user_name != "broiestbro":
            room.message(
                "SIGN THE PETITION: \
                                https://www.change.org/p/nhl-exclude-penguins-from-bird-team-classification \
                                https://i.imgur.com/nYQy0GR.jpg",
            )
        elif chat_message.endswith("only on aclee"):
            room.message("™")
        elif chat_message.lower() == "tm":
            self._trademark(room, message)
        elif chat_message.lower().replace("'", "") == "anyway heres wonderwall":
            room.message("https://i.imgur.com/Z64dNAn.jpg https://www.youtube.com/watch?v=bx1Bh8ZvH84")
        # elif re.search(r"instagram.com/p/[a-zA-Z0-9_-]+", message.body):
        # self._create_link_preview(room, message.body)
        LOGGER.info(f"[{room.room_name}] [{user_name}] [{message.ip}]: {message.body}")

    @staticmethod
    def _get_user_data(room_name: str, user: User, message: Message) -> None:
        """
        Persist metadata regarding message history.

        :param str room_name: Chatango room.
        :param User user: User responsible for triggering command.
        :param Message message: User submitted message.

        :returns: None
        """
        try:
            if message.ip:
                existing_user = (
                    session.query(ChatangoUser)
                    .filter(
                        ChatangoUser.username == user.name.lower(),
                        ChatangoUser.chatango_room == room_name,
                        ChatangoUser.ip == message.ip,
                    )
                    .first()
                )
                if existing_user is None:
                    user_metadata = geo.lookup_user(message.ip)
                    # fmt: off
                    session.add(
                        ChatangoUser(
                            username=user.name.lower().replace("!anon", "anon"),
                            chatango_room=room_name,
                            city=user_metadata.get("city"),
                            region=user_metadata.get("region"),
                            country_name=user_metadata.get("country_name"),
                            latitude=user_metadata.get("latitude"),
                            longitude=user_metadata.get("longitude"),
                            postal=user_metadata.get("postal"),
                            emoji_flag=user_metadata.get("emoji_flag"),
                            status=user_metadata.get("status"),
                            time_zone_name=user_metadata.get("time_zone").get("name") if user_metadata.get("time_zone") else None,
                            time_zone_abbr=user_metadata.get("time_zone").get("abbr") if user_metadata.get("time_zone") else None,
                            time_zone_offset=user_metadata.get("time_zone").get("offset") if user_metadata.get("time_zone") else None,
                            time_zone_is_dst=user_metadata.get("time_zone").get("is_dst") if user_metadata.get("time_zone") else None,
                            carrier_name=user_metadata.get("carrier").get("name") if user_metadata.get("carrier") else None,
                            carrier_mnc=user_metadata.get("carrier").get("mnc") if user_metadata.get("carrier") else None,
                            carrier_mcc=user_metadata.get("carrier").get("mcc") if user_metadata.get("carrier") else None,
                            asn_asn=user_metadata.get("asn").get("asn") if user_metadata.get("asn") else None,
                            asn_name=user_metadata.get("asn").get("name") if user_metadata.get("asn") else None,
                            asn_domain=user_metadata.get("asn").get("domain") if user_metadata.get("asn") else None,
                            asn_route=user_metadata.get("asn").get("route") if user_metadata.get("asn") else None,
                            asn_type=user_metadata.get("asn").get("type") if user_metadata.get("asn") else None,
                            time_zone_current_time=user_metadata.get("time_zone").get("current_time") if user_metadata.get("time_zone") else None,
                            ip=message.ip
                        )
                    )
                    # fmt: on
        except IncompatibleParameters as e:
            LOGGER.warning(f"Failed to save data for {user.name} due to IncompatibleParameters: {e}")
        except Exception as e:
            LOGGER.warning(f"Unexpected error while attempting to save data for {user.name}: {e}")

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

    def _get_response(self, chat_message: str, room: Room, user_name: str) -> Optional[str]:
        """
        Fetch response from database to send to chat.

        :param str chat_message: Raw message sent by user.
        :param Room room: Chatango room.
        :param str user_name: User responsible for triggering command.

        :returns: Optional[str]
        """
        cmd, args = self._parse_command(chat_message[1::])
        command = session.query(Command).filter(Command.command == cmd).first()
        if command is not None:
            response = self.create_message(
                command.type,
                command.response,
                command=cmd,
                args=args,
                room=room,
                user_name=user_name,
            )
            room.message(response, html=True)
        else:
            self._giphy_fallback(chat_message, room)

    @staticmethod
    def _create_link_preview(room: Room, url: str) -> None:
        """
        Generate link preview for Instagram post URL.

        :param Room room: Chatango room.
        :param str url: URL of an Instagram post.

        :returns: None
        """
        preview = create_instagram_preview(url)
        room.message(preview)

    @staticmethod
    def _bot_status_check(room: Room) -> None:
        """
        Check bot status.

        :param Room room: Chatango room.

        :returns: None
        """
        room.message("hellouughhgughhg?")

    @staticmethod
    def _wave_back(room: Room, user_name: str) -> None:
        """
        Wave back at user.

        :param Room room: Chatango room.
        :param str user_name: User name of Chatango user who waved.

        :returns: None
        """
        if user_name == "broiestbro":
            room.message(f"stop talking to urself and get some friends u fuckin loser jfc kys @broiestbro")
        else:
            room.message(f"@{user_name} *waves*")

    @staticmethod
    def _giphy_fallback(message: str, room: Room) -> None:
        """
        Default to Giphy for non-existent commands.

        :param str message: Command triggered by a user.
        :param Room room: Chatango room.

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

        :param Room room: Chatango room.
        :param Message message: Message sent by user.
        :param str user_name: User responsible for triggering command.
        :param bool silent: Whether or not offending user should be warned.

        :returns: None
        """
        message.delete()
        if silent is False:
            room.message(f"DO NOT SAY THAT WORD @{user_name.upper()} :@")

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
    def _check_blacklisted_users(room: Room, user_name: str, message: Message) -> None:
        """
        Ban and delete chat history of blacklisted user.

        :param Room room: Chatango room name.
        :param str user_name: Chatango username to validate against blacklist.
        :param Message message: User submitted message.

        :returns: None
        """
        if user_name in CHATANGO_BLACKLISTED_USERS:
            room.ban(message)
            reply = emojize(
                f":wave: @{user_name} lmao pz fgt have fun being banned forever :wave:",
                use_aliases=True,
            )
            room.message(reply)
