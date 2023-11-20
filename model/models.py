from requests import Session
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Date, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

Base = declarative_base()


class Topic(Base):
    __tablename__ = 'links'
    __tableargs__ = {
        'comment': 'Ссылки'
    }

    id = Column(
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    url = Column(String, comment='Адрес картинки', unique=True)
    print(url)
    content_type = Column(String)
    chanel_id = Column(String)


class Replay(Base):
    __tablename__ = 'replay'
    __tableargs__ = {
        'comment': 'повторяющиеся ссылки'
    }

    id = Column(
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    url = Column(String, comment='Адрес картинки', unique=True)
    content_type = Column(String)
    date_update = Column(
        DateTime(timezone=True), default=func.now(),
        nullable=False, onupdate=func.now()
    )
    chanel_id = Column(String)
