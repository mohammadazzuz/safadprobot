# SQLAlchemy models
from sqlalchemy import Column, String, BigInteger, JSON
from .database import Base

class GuildSettings(Base):
    __tablename__ = "guild_settings"

    guild_id = Column(BigInteger, primary_key=True, index=True)
    welcome_channel_id = Column(String, default="")
    welcome_message = Column(String, default="")
    user_xp = Column(JSON, default={})
    user_level = Column(JSON, default={})
    weapon_classes = Column(JSON, default={})

class User(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True, index=True)
    discord_name = Column(String)
    guild_id = Column(BigInteger)