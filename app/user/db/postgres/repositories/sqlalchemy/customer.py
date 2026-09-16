from typing import Optional
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.shared.db.postgres.repositories.sqlalchemy.repository import BaseSQLAlchemyREPO
from app.user.db.postgres.models import UserModel, UserRoleENUM

class CustomerSQLAlchemyREPO(BaseSQLAlchemyREPO[UserModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            model=UserModel
        )

    async def get_by_email_and_inactive(self, email: str) -> Optional[UserModel]:
        stmt = select(self.model).where(
            func.lower(self.model.email) == email.lower(),
            self.model.is_active.is_(False),
            self.model.role == UserRoleENUM.CUSTOMER
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[UserModel]:
        stmt = select(self.model).where(
            func.lower(self.model.email) == email.lower(),
            self.model.role == UserRoleENUM.CUSTOMER
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_email_and_active(self, email: str) -> Optional[UserModel]:
        stmt = select(self.model).where(
            func.lower(self.model.email) == email.lower(),
            self.model.is_active.is_(True),
            self.model.role == UserRoleENUM.CUSTOMER
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()