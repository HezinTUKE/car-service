import sqlalchemy.ext.declarative as dec
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from application import config

Base = dec.declarative_base()


class DBModel:
    config_db = config.database
    db_url = f"""postgresql+asyncpg://{config_db.username}:{config_db.password}@{config_db.host}:{config_db.port}/{config_db.db_name}"""
    engine = create_async_engine(db_url, connect_args={})

    @classmethod
    async def get_session(cls, commit: bool = True):
        session = AsyncSession(cls.engine)
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
