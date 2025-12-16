from fastapi import FastAPI

from application.controllers.login import LoginController


def run():
    app = FastAPI()
    app.include_router(LoginController.router)
