import time
import uuid

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UUID, String, Integer

from application.enums.roles import Roles
from application.models.base import Base
from application.utils.type_decorators import EnumAsVarchar


class UsersModel(Base):
    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(String, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String, index=True, nullable=False)
    created_at: Mapped[int] = mapped_column(Integer, index=True, default=int(time.time()))
    updated_at: Mapped[int] = mapped_column(Integer, index=True, default=int(time.time()), onupdate=int(time.time()))
    role: Mapped[Roles] = mapped_column(EnumAsVarchar(Roles, length=10), default=Roles.USER, index=True, nullable=False)
