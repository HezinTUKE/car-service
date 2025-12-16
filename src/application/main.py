from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from application.controllers.login import LoginController

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()
app.include_router(LoginController.router)
