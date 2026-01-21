from logging.config import dictConfig

from fastapi import FastAPI

from application import config
from application.controllers.login import LoginController
from application.controllers.opensearch_controller import OpensearchController
from application.controllers.services.offer_controller import OfferController
from application.controllers.services.organization_controller import OrganizationController
from application.controllers.services.service_controller import ServiceController


dictConfig(config.log_config)

app = FastAPI()
app.include_router(LoginController.router)
app.include_router(ServiceController.router)
app.include_router(OrganizationController.router)
app.include_router(OfferController.router)
app.include_router(OpensearchController.router)
