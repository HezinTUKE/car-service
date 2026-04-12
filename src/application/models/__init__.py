from sqlalchemy.orm import configure_mappers

from application.models.users.user_setup import UserSetupModel
from application.models.users.user_car_relation import UserCarRelationModel
from application.models.services.service import ServiceModel
from application.models.services.organization import OrganizationModel
from application.models.services.offer import OfferModel
from application.models.cars.car_brand import CarBrandModel
from application.models.cars.car_type import CarTypeModel
from application.models.cars.engine_type import EngineTypeModel
from application.models.translations.description import OfferDescriptionModel, ServiceDescriptionModel, OrganizationDescriptionModel
from application.models.translations.relation_translated_offer import RelationTranslatedOfferModel
from application.models.translations.offer_type_translations import OfferTypeTranslationsModel
from application.models.base import Base

configure_mappers()

__all__ = [
    "Base",
    "ServiceModel",
    "OrganizationModel",
    "OfferModel",
    "CarTypeModel",
    "CarBrandModel",
    "EngineTypeModel",
    "OfferTypeTranslationsModel",
    "RelationTranslatedOfferModel",
    "UserSetupModel",
    "UserCarRelationModel",
    "OfferDescriptionModel",
    "ServiceDescriptionModel",
    "OrganizationDescriptionModel"
]
