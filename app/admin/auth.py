from sqladmin.authentication import AuthenticationBackend
from fastapi import Request
from sqlalchemy import select
from app.core.config.base import get_settings
from app.core.db.postgres import db_helper
from app.user.service.infrastructure.user.check_password import user_check_password
from app.user.db.postgres.models import UserModel, UserRoleENUM

class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()

        email = form.get("email")
        password = form.get("password")

        if not email or not password:
            return False

        async with db_helper.session_factory() as session:
            user = await self._get_user(session, email)

            if not user:
                return False
            if not user.is_active:
                return False
            if user.role != UserRoleENUM.ADMIN:
                return False
            if not user_check_password(
                password,
                user.password
            ):
                return False

            request.session.update(
                {"admin_id": str(user.id)}
            )

            return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        admin_id = request.session.get("admin_id")

        if not admin_id:
            return False

        async with db_helper.session_factory() as session:
            user = await session.get(
                UserModel,
                int(admin_id)
            )

            if not user:
                return False
            if not user.is_active:
                return False
            if user.role != UserRoleENUM.ADMIN:
                return False
        return True

    async def _get_user(
        self,
        session,
        email: str
    ) -> UserModel | None:
        result = await session.execute(
            select(UserModel)
            .where(UserModel.email == email)
        )
        return result.scalar_one_or_none()


settings = get_settings()
authentication_backend = AdminAuth(
    secret_key=settings.app.secret_key
)