from fastapi import APIRouter

from application.controllers.cms.cms_car_controller import CMSCarController


class CMSController:
    router = APIRouter(prefix="/cms", tags=["cms"])

    router.include_router(CMSCarController.router)
