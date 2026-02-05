from fastapi import APIRouter


class ScheduleController:
    router = APIRouter(prefix="/schedule", tags=["Schedule"])

    @staticmethod
    @router.get("/midnight")
    async def midnight_event():
        pass
