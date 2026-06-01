from sqlalchemy.orm import configure_mappers

from application.models.payments.product import ProductModel
from application.models.users.user_setup import UserSetupModel
from application.models.users.user_car_relation import UserCarRelationModel
from application.models.services.service import ServiceModel
from application.models.services.organization import OrganizationModel
from application.models.offers.offer import OfferModel
from application.models.cars.car_brand import CarBrandModel
from application.models.cars.car_model import CarTypeModel
from application.models.cars.engine_type import EngineTypeModel
from application.models.cars.car_engine_relation import CarEngineRelationModel
from application.models.offers.offer_group import OfferGroupModel
from application.models.offers.service_offer_group import ServiceOfferGroup
from application.models.base import Base

configure_mappers()

__all__ = [
    "Base",
    "ProductModel",
    "ServiceModel",
    "OrganizationModel",
    "OfferModel",
    "CarTypeModel",
    "CarBrandModel",
    "CarEngineRelationModel",
    "EngineTypeModel",
    "UserSetupModel",
    "UserCarRelationModel",
    "OfferModel",
    "OfferGroupModel",
    "ServiceOfferGroup"
]
