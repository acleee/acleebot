from sqlalchemy import Column, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

from database import engine

Base = declarative_base()


class Chat(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False)
    room = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"time={self.created_at}, room={self.room}, username={self.username}, chat={self.message}"


class Command(Base):
    __tablename__ = "commands"

    id = Column(Integer, primary_key=True, index=True)
    command = Column(String(255), nullable=False, unique=True, index=True)
    type = Column(String(255), nullable=False)
    response = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"command={self.command}, type={self.type}, response={self.response}"


class ChatangoUser(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255))
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
    carrier = Column(Text)
    carrier_name = Column(String(255))
    carrier_mnc = Column(Text)
    carrier_mcc = Column(Text)
    asn_asn = Column(Text)
    asn_name = Column(String(255))
    asn_domain = Column(String(255))
    asn_route = Column(String(255))
    asn_type = Column(String(255))
    time_zone_current_time = Column(DateTime)
    threat_is_tor = Column(Integer)
    threat_is_proxy = Column(Integer)
    threat_is_anonymous = Column(Integer)
    threat_is_known_attacker = Column(Integer)
    threat_is_known_abuser = Column(Integer)
    threat_is_threat = Column(Integer)
    threat_is_bogon = Column(Integer)

    def __repr__(self):
        return f"username={self.username}, chatango_room={self.chatango_room}, city={self.city}, region={self.region}, country_name={self.country_name}"


Base.metadata.create_all(engine)
