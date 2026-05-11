from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from application.configs import settings


engine = create_async_engine(
    settings.DB_URL,
    future=True,
    echo=True,
)

SessionFactory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)
