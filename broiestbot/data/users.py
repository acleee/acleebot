"""Persist user metadata."""
from typing import Optional
from datetime import datetime

from database import session_rw
from database.models import ChatangoUser
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from chatango.ch import Message, User
from clients import geo
from config import PERSIST_USER_DATA
from logger import LOGGER


def persist_user_data(room_name: str, user: User, message: Message, bot_username: str) -> None:
    """
    Persist user metadata.

    :param str room_name: Chatango room.
    :param User user: User responsible for triggering command.
    :param Message message: User submitted message.
    :param str bot_username: Name of the currently run bot.

    :returns: None
    """
    try:
        if message.ip and PERSIST_USER_DATA and bot_username in ("broiestbro", "broiestbot"):
            existing_user = fetch_existing_user(room_name, user, message)
            if existing_user is None:
                user_metadata = geo.lookup_user(message.ip)
                # fmt: off
                session_rw.add(
                    ChatangoUser(
                        username=user.name.lower().replace("!anon", "anon"),
                        chatango_room=room_name,
                        city=user_metadata.get("city"),
                        ip=message.ip,
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
                        is_proxy=user_metadata.get("threat").get("is_proxy"),
                        is_anonymous=user_metadata.get("threat").get("is_anonymous"),
                        is_tor=user_metadata.get("threat").get("is_tor"),
                        is_known_attacker=user_metadata.get("threat").get("is_known_attacker"),
                        is_known_abuser=user_metadata.get("threat").get("is_known_abuser"),
                        created_at=datetime.now()
                    )
                )
                # fmt: on
    except IntegrityError as e:
        LOGGER.error(f"Failed to save duplicate entry for {user.name}: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error while attempting to save data for {user.name}: {e}")


def fetch_existing_user(room_name: str, user: User, message: Message) -> Optional[ChatangoUser]:
    """
    Persist metadata regarding message history.

    :param str room_name: Chatango room.
    :param User user: User responsible for triggering command.
    :param Message message: User submitted message.

    :returns: Optional[ChatangoUser]
    """
    try:
        if message.ip:
            return (
                session_rw.query(ChatangoUser)
                .filter(
                    ChatangoUser.username == user.name.lower(),
                    ChatangoUser.chatango_room == room_name,
                    ChatangoUser.ip == message.ip,
                )
                .first()
            )
    except SQLAlchemyError as e:
        LOGGER.warning(f"SQLAlchemyError occurred while fetching metadata for {user.name}: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error while attempting to save data for {user.name}: {e}")
