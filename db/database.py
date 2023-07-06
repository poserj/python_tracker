from helpers import init_db
from sqlmodel import SQLModel, create_engine


def create_tables():
    db_conf = init_db()
    engine = create_engine(db_conf['DATABASE_URL'], echo=db_conf['DEBUG_MOD'])
    SQLModel.metadata.create_all(engine)


if __name__ == '__main__':
    create_tables()
