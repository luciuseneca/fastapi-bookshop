from typing import Optional
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.shared.db.postgres.repositories.sqlalchemy.repository import BaseSQLAlchemyREPO
from app.user.db.postgres.models import UserModel, UserRoleENUM

class ManagerSQLAlchemyRepository(BaseSQLAlchemyREPO[UserModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            model=UserModel
        )

    async def get_by_id(self, manager_id: int) -> Optional[UserModel]:
        stmt = select(UserModel).where(
            UserModel.id == manager_id,
            UserModel.role == UserRoleENUM.MANAGER
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[UserModel]:
        stmt = select(UserModel).where(
            UserModel.email == email,
            UserModel.role == UserRoleENUM.MANAGER
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()