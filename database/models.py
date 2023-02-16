"""Define data models for chat commands, phrases, user logs, etc."""
from database import engine_ro, engine_rw
from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

BaseRW = declarative_base()
BaseRO = declarative_base()


class Chat(BaseRW):
    """Single chat (from a user) to persist in logs."""

    __tablename__ = "chat"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False)
    room = Column(String(255), nullable=False, index=True)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"time={self.created_at}, room={self.room}, username={self.username}, chat={self.message}"


class Command(BaseRO):
    """Bot commands triggered by `!` prefix."""

    __tablename__ = "commands"

    id = Column(Integer, primary_key=True, index=True)
    command = Column(String(255), nullable=False, unique=True, index=True)
    type = Column(String(255), nullable=False)
    response = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"command={self.command}, type={self.type}, response={self.response}"


class Phrase(BaseRO):
    """Reserved phrases which trigger a response."""

    __tablename__ = "phrases"

    id = Column(Integer, primary_key=True, index=True)
    phrase = Column(String(255), nullable=False, unique=True, index=True)
    response = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"command={self.phrase}, type={self.response}"


class ChatangoUser(BaseRW):
    """Chatango user metadata."""

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), index=True)
    chatango_room = Column(String(255))
    ip = Column(String(255), index=True)
    city = Column(String(255))
    region = Column(String(255))
    country_name = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
    postal = Column(String(255))
    emoji_flag = Column(Text)
    status = Column(Integer)
    time_zone_name = Column(String(255))
    time_zone_abbr = Column(String(255))
    time_zone_offset = Column(Integer)
    time_zone_is_dst = Column(Integer)
    carrier_name = Column(String(255))
    carrier_mnc = Column(Text)
    carrier_mcc = Column(Text)
    asn_asn = Column(Text)
    asn_name = Column(String(255))
    asn_domain = Column(String(255))
    asn_route = Column(String(255))
    asn_type = Column(String(255))
    time_zone_current_time = Column(DateTime)
    is_proxy = Column(Boolean)
    is_anonymous = Column(Boolean)
    is_tor = Column(Boolean)
    is_known_attacker = Column(Boolean)
    is_known_abuser = Column(Boolean)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    def __repr__(self):
        return f"username={self.username}, chatango_room={self.chatango_room}, city={self.city}, region={self.ip}"


class Weather(BaseRO):
    """Mapping of weather emojis to weather conditions."""

    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(Integer, nullable=False)
    condition = Column(Text, nullable=False)
    icon = Column(String(255), nullable=False)
    group = Column(String(255), nullable=False)

    def __repr__(self):
        return f"group={self.group}, icon={self.icon}, condition={self.condition}"


class PollResult(BaseRW):
    """Result of a poll or counter."""

    __tablename__ = "poll"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(255), nullable=False, index=True, unique=True)
    count = Column(Integer)
    updated_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"type={self.type}, count={self.count}, updated_at={self.updated_at}"


BaseRO.metadata.create_all(engine_ro)
BaseRW.metadata.create_all(engine_rw)
