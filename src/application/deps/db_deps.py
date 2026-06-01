from typing import AsyncContextManager

from loguru import logger

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from application.models.engine import SessionFactory
from application.utils.exceptions import DBException


def get_context_session() -> AsyncContextManager[AsyncSession]:
    return SessionFactory()


async def get_session():
    async with SessionFactory() as session:
        try:
            yield session
        except SQLAlchemyError:
            await session.rollback()
            logger.exception("DB Exception", exc_info=True)
            raise DBException
