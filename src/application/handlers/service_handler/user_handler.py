from sqlalchemy.ext.asyncio import AsyncSession

from application.models import UserSetupModel
from application.schemas.service_schemas.request_schemas.user_setup_schema import CreateUserSetupSchema


class UserHandler:
    @staticmethod
    async def create_user_setup(session: AsyncSession, user_setup: CreateUserSetupSchema, user_id: str):
        model = UserSetupModel(
            user_id=user_id,
            name=user_setup.name,
            surname=user_setup.surname,
        )

        session.add(model)
        await session.commit()
