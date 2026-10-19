from fastapi import (
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.api.dependencies import auth_manager
from app.user.api.requests.customer.auth import CustomerAuthorizedREQT
from app.user.db.postgres.models import UserModel, UserRoleENUM
from app.core.db.postgres import db_helper


async def get_current_manager(
    payload: CustomerAuthorizedREQT = Depends(auth_manager),
    db: AsyncSession = Depends(db_helper.session_getter),
) -> UserModel:
    """Двухуровневая проверка менеджера: роль в JWT (auth_manager),
    затем актуальная роль и активность в БД."""
    user = await db.get(UserModel, int(payload.sub))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Customer not found",
        )

    if user.role != UserRoleENUM.MANAGER or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only managers allowed",
        )

    return user
