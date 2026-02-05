from contextlib import asynccontextmanager
from logging.config import dictConfig

from fastapi import FastAPI

from application import config
from application.controllers.login import LoginController
from application.controllers.services.offer_controller import OfferController
from application.controllers.services.organization_controller import OrganizationController
from application.controllers.services.service_controller import ServiceController
from application.events.event import get_rabbit_processor, close_rabbit_processor


@asynccontextmanager
async def lifespan(_: FastAPI):
    rabbitmq = await get_rabbit_processor()
    await rabbitmq.listen()

    try:
        yield
    finally:
        await close_rabbit_processor()


dictConfig(config.log_config)

app = FastAPI(lifespan=lifespan)
app.include_router(LoginController.router)
app.include_router(ServiceController.router)
app.include_router(OrganizationController.router)
app.include_router(OfferController.router)
