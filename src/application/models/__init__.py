from sqlalchemy.orm import configure_mappers

from application.models.users_model import UsersModel
from application.models.services.service import ServiceModel
from application.models.services.organization import OrganizationModel
from application.models.services.offer import OfferModel
from application.models.services.offer_car_compatibility import OfferCarCompatibilityModel
from application.models.base import Base

configure_mappers()

__all__ = ["Base", "UsersModel", "ServiceModel", "OrganizationModel", "OfferModel", "OfferCarCompatibilityModel"]
