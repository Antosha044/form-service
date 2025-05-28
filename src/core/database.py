from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from src.settings import settings

engine = create_async_engine(
    url = settings.DATABASE_URL_asyncpg,
    echo = True
)

async_session_factory = async_sessionmaker(
    bind = engine,
    expire_on_commit = False,
    class_ = AsyncSession
)

async def get_db():
    async with async_session_factory() as session:
        yield session

class Base(DeclarativeBase):
    pass
