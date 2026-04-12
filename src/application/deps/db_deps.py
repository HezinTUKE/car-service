from loguru import logger

from sqlalchemy.exc import SQLAlchemyError

from application.models.engine import SessionFactory
from application.utils.exceptions import DBException


async def get_session():
    async with SessionFactory() as session:
        try:
            yield session
        except SQLAlchemyError:
            await session.rollback()
            logger.error("DB Exception", exc_info=True)
            raise DBException
