from sqlalchemy.orm import configure_mappers

from application.models.users_model import UsersModel
from application.models.base import Base

configure_mappers()

__all__ = [
    "Base",
    "UsersModel",
]
