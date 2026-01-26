import logging

from fastapi import HTTPException, status

from application.models.engine import SessionFactory


class DBModel:
    logger = logging.getLogger(" ")

    @classmethod
    async def get_session(cls):
        async with SessionFactory() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                cls.logger.error("DB Exception", exc_info=True)
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="DB Exception")
