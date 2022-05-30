import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.orm import sessionmaker
from db.db import Db
from asyncio import get_event_loop


@pytest_asyncio.fixture(scope="session")
def event_loop():
    return get_event_loop()


@pytest_asyncio.fixture(scope="session")
async def db_object():
    url = "postgresql+asyncpg://postgres:postgres@db/maindb"
    db = Db(url)
    await db.drop_tables()
    await db.init_tables()
    yield db.engine
    await db.engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def session_maker(db_object: AsyncEngine):
    session_local = sessionmaker(db_object, class_=AsyncSession,
                                 autoflush=False)
    return session_local


@pytest_asyncio.fixture()
async def create_session(session_maker: sessionmaker):
    async with session_maker() as session:
        yield session
