from typing import AsyncGenerator

import yaml
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


def init_db():
    with open("config.yaml", "r") as stream:
        try:
            data = yaml.safe_load(stream)
            return data['DB']
        except yaml.YAMLError as exc:
            raise yaml.YAMLError


async def get_session() -> AsyncGenerator:
    async with AsyncSession(engine) as session:
        yield session


config = init_db()
engine = create_async_engine(config['DATABASE_URL'], echo=config['DEBUG_MOD'])
