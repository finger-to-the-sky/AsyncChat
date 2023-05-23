from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from database import Base
from datetime import datetime


class Users(Base):
    """
    Модель Пользователей:
    username: имя пользователя
    last_login: дата последнего посещения
    """

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    last_login = Column(DateTime, default=datetime.now())


class ActiveUsers(Base):
    """
    Модель Активности пользователя:
    ip_address - ip адрес
    port - порт
    login_time - Дата и время посещения
    """

    __tablename__ = 'active_users'
    id = Column(Integer, primary_key=True, index=True)
    user_id = ForeignKey('Users.id', unique=True)
    ip_address = Column(String)
    port = Column(Integer)
    login_time = Column(DateTime)


class History(Base):
    """
    Модель истории активности пользователей:
    username - имя пользователя
    date - Дата и время посещения
    ip - ip адрес
    port - порт
    """

    __tablename__ = 'history'
    id = Column(Integer, primary_key=True, index=True)
    user_id = ForeignKey('Users.id')
    username = Column(String)
    date = Column(DateTime)
    ip = Column(String)
    port = Column(Integer)
