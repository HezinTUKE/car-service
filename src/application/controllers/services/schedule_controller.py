from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.deps.db_deps import DBModel
from application.handlers.service_handler.publish_services_handler import PublishServicesHandler


class ScheduleController:
    router = APIRouter(prefix="/schedule", tags=["Schedule"])

    @staticmethod
    @router.get("/midnight")
    async def midnight_event(
        session: AsyncSession = Depends(DBModel.get_session),
    ):
        res = await PublishServicesHandler.publish_services(session)
        return res
