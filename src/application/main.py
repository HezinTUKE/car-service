import logging

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from application.controllers.login import LoginController
from application.controllers.services.service_controller import ServiceController

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

app = FastAPI()
app.include_router(LoginController.router)
app.include_router(ServiceController.router)
