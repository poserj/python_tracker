from helpers import init_db
from sqlmodel import SQLModel, create_engine


def create_tables():
    db_conf = init_db()
    engine = create_engine(db_conf['DATABASE_URL'], echo=db_conf['DEBUG_MOD'])
    SQLModel.metadata.create_all(engine)
    from alembic import command
    from alembic.config import Config

    alembic_cfg = Config('db/migrations/alembic.ini')
    command.stamp(alembic_cfg, 'head')


if __name__ == '__main__':
    create_tables()
