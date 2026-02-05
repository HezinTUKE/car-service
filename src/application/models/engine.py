from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from application import config


config_db = config.database
db_url = f"""postgresql+asyncpg://{config_db.username}:{config_db.password}@{config_db.host}:{config_db.port}/{config_db.db_name}"""

engine = create_async_engine(
    db_url,
    future=True,
)

SessionFactory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)
