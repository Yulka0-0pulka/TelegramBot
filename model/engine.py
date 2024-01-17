from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from model.models import Base
from config.setting import setting

engine = create_engine(setting.BUILD_URL)
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
