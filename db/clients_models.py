from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime


class Base(DeclarativeBase):
    pass


class KnownUsers(Base):
    __tablename__ = 'known_users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)


class MessageHistory(Base):
    __tablename__ = 'message_history'
    id = Column(Integer, primary_key=True, index=True)
    from_user = Column(String)
    to_user = Column(String)
    message = Column(Text)
    date = Column(DateTime)


class Contacts(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
