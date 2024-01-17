from typing import Literal
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from model.models import Base
from pydantic.v1 import BaseSettings
from environs import Env

env = Env()
environment: Literal["docker", "local"] = "docker"
if environment == "docker":
    env.read_env(path="./docker/.env")
else:
    env.read_env(path=".env")


class Setting(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    PSQL_HOST: str
    PSQL_PORT: str
    POSTGRES_DB: str
    BUILD_URL: str = None


s = Setting()

engine = create_engine(
    f"postgresql+psycopg2://{s.POSTGRES_USER}:"
    f"{s.POSTGRES_PASSWORD}@{s.PSQL_HOST}:"
    f"{s.PSQL_PORT}/{s.POSTGRES_DB}")
session = Session(bind=engine)


def db_session() -> sessionmaker[Session]:
    s = sessionmaker(bind=engine)
    return s


def insert_image(url, content_type, model, chanel_id) -> None:
    session: sessionmaker[Session] = db_session()
    with session() as sess:
        instance = model(url=url, content_type=content_type,
                         chanel_id=chanel_id)
        sess.add(instance)
        sess.commit()


if __name__ == "__main__":
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print("Создание базы выполненно успешно")
