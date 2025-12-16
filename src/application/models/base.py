import sqlalchemy.ext.declarative as dec
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from application import config

Base = dec.declarative_base()

class DBModel:
    config_db = config["database"]
    db_url = f"""postgresql+asyncpg://{config_db.get("username")}:{config_db.get("password")}@{config_db.get("host")}:{config_db.get("port")}/{config_db.get("db_name")}"""
    engine = create_async_engine(db_url, connect_args={})

    @classmethod
    async def get_session(cls):
        session = AsyncSession(cls.engine)
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
