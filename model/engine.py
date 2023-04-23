from email import message
from gettext import dpgettext
from xml.parsers.expat import model
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from aiogram import Bot, types
from data.config import BOT_TOKEN


from model.models import Base, Topic
engine = create_engine(
    "postgresql+psycopg2://postgres:postgres@localhost:5444/db_test")
session = Session(bind=engine)


def db_session() -> sessionmaker[Session]:
    s = sessionmaker(bind=engine)
    return s


def insert_image(url, content_type, model, chanel_id) -> None:
    session: sessionmaker[Session] = db_session()
    with session() as sess:
        instance = model(url=url, content_type=content_type, chanel_id=chanel_id)
        sess.add(instance)
        sess.commit()  # type: ignore


if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
