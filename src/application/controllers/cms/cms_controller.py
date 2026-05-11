from fastapi import APIRouter

from application.controllers.cms.cms_car_controller import CMSCarController
from application.controllers.cms.cms_payment_controller import PaymentController
from application.controllers.cms.cms_service_controller import CMSServiceController
from application.controllers.services.offer_controller import OfferController


class CMSController:
    router = APIRouter(prefix="/cms", tags=["cms"])

    router.include_router(CMSCarController.router)
    router.include_router(PaymentController.router)
    router.include_router(CMSServiceController.router)
