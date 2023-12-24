from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


from model.models import Base
engine = create_engine(
    "postgresql+psycopg2://postgres:postgres@localhost:5454/db_telegram")
session = Session(bind=engine)


def db_session() -> sessionmaker[Session]:
    s = sessionmaker(bind=engine)
    return s


def insert_image(url, content_type, model, chanel_id) -> None:
    session: sessionmaker[Session] = db_session()
    with session() as sess:
        instance = model(url=url, content_type=content_type, chanel_id=chanel_id)
        sess.add(instance)
        sess.commit() 


if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
