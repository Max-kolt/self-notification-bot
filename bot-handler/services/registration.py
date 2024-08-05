from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from database import User


class UserSchema(BaseModel):
    telegram_id: int
    name: str
    email: str


class RegistrationService:
    @staticmethod
    async def verify(session: AsyncSession, telegram_id: int) -> bool | None:
        """
        Checking user registration
        :param session: Database session
        :param telegram_id: User telegram id
        :return: bool
        """
        query = select(User).where(User.telegram_id == telegram_id)
        result = (await session.execute(query)).scalar_one_or_none()
        if result:
            return True

    @staticmethod
    async def registration(session: AsyncSession, user_data: UserSchema) -> bool:
        """
        Saving and registering the user
        :param session: Database session
        :param user_data: User information to register
        :return: bool
        """
        new_user = User(**user_data.model_dump())
        session.add(new_user)
        await session.commit()
        return True

