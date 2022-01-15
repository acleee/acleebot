from sqlalchemy import Column, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

from database import engine

Base = declarative_base()


class Chat(Base):
    """Chatango user chat to persist in logs."""

    __tablename__ = "chat"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False)
    room = Column(String(255), nullable=False, index=True)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"time={self.created_at}, room={self.room}, username={self.username}, chat={self.message}"


class Command(Base):
    """Bot commands triggered by `!` prefix upon chat."""

    __tablename__ = "commands"

    id = Column(Integer, primary_key=True, index=True)
    command = Column(String(255), nullable=False, unique=True, index=True)
    type = Column(String(255), nullable=False)
    response = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"command={self.command}, type={self.type}, response={self.response}"


class Phrase(Base):
    """Reserved phrases which prompt a response (no `!` required)."""

    __tablename__ = "phrases"

    id = Column(Integer, primary_key=True, index=True)
    phrase = Column(String(255), nullable=False, unique=True, index=True)
    response = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"command={self.phrase}, type={self.response}"


class ChatangoUser(Base):
    """Chatango user metadata for anon auditing purposes."""

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), index=True)
    chatango_room = Column(String(255))
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
    ip = Column(String(255), index=True)

    def __repr__(self):
        return f"username={self.username}, chatango_room={self.chatango_room}, city={self.city}, region={self.ip}"


Base.metadata.create_all(engine)
