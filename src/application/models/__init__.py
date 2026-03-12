from sqlalchemy.orm import configure_mappers

from application.models.users_model import UsersModel
from application.models.services.service import ServiceModel
from application.models.services.organization import OrganizationModel
from application.models.services.offer import OfferModel
from application.models.services.car_brand import CarBrandModel
from application.models.services.car_type import CarTypeModel
from application.models.services.engine_type import EngineTypeModel
from application.models.services.offer_car_compatibility import OfferCarCompatibilityModel
from application.models.services.relation_translated_offer import RelationTranslatedOfferModel
from application.models.services.offer_type_translations import OfferTypeTranslationsModel
from application.models.base import Base

configure_mappers()

__all__ = [
    "Base",
    "UsersModel",
    "ServiceModel",
    "OrganizationModel",
    "OfferModel",
    "OfferCarCompatibilityModel",
    "CarTypeModel",
    "CarBrandModel",
    "EngineTypeModel",
    "OfferTypeTranslationsModel",
    "RelationTranslatedOfferModel",
]
