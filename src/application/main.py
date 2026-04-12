from contextlib import asynccontextmanager
from loguru import logger

from fastapi import FastAPI

from application.controllers.cms.cms_controller import CMSController
from application.controllers.login import LoginController
from application.controllers.services.offer_controller import OfferController
from application.controllers.services.organization_controller import OrganizationController
from application.controllers.services.schedule_controller import ScheduleController
from application.controllers.services.service_controller import ServiceController
from application.controllers.services.user_controller import UserController
from application.events.event import get_rabbit_processor, close_rabbit_processor


@asynccontextmanager
async def lifespan(_: FastAPI):
    rabbitmq = await get_rabbit_processor()
    await rabbitmq.listen()

    try:
        yield
    finally:
        await close_rabbit_processor()


logger.add("debug.log", rotation="100 MB")

app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def all_loggers(request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code} for {request.method} {request.url}")
    return response

app.include_router(UserController.router)
app.include_router(LoginController.router)
app.include_router(ServiceController.router)
app.include_router(OrganizationController.router)
app.include_router(OfferController.router)
app.include_router(ScheduleController.router)
app.include_router(CMSController.router)
