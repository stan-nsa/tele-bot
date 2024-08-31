from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from config import config
from db.models import Base

engine_sqlite = create_async_engine(url=f"sqlite+aiosqlite:///{config.db.database}", echo=True)

engine = engine_sqlite

db_session = async_sessionmaker(bind=engine, class_=AsyncSession)  # , expire_on_commit=False)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
