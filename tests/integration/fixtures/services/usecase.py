import pytest_asyncio
from app.user.service.usecase.jwt.refresh_update import JwtRefreshTokenUpdateUC
from app.user.service.usecase.ouath.google_authorization import CustomerGoogleAuthorizationUC
from app.user.service.usecase.customer.authentication import CustomerAuthenticationUC
from app.user.service.usecase.customer.authorization import CustomerAuthorizationUC
from app.user.service.usecase.customer.logout import CustomerLogoutUC
from app.core.config.base import get_settings

# client
@pytest_asyncio.fixture(scope="function")
def user_authentication_usecase(
    transaction,
    user_repository,
    otp_auth_session,
):
    settings = get_settings()

    return CustomerAuthenticationUC(
        transaction=transaction,
        user_repository=user_repository,
        otp_auth_session=otp_auth_session,
        settings=settings,
    )


@pytest_asyncio.fixture(scope="function")
def user_authorization_usecase(
    transaction,
    user_repository,
    otp_auth_session,
    jwt_refresh_session,
    jwt_generator,
):
    settings = get_settings()

    return CustomerAuthorizationUC(
        transaction=transaction,
        user_repository=user_repository,
        otp_auth_session=otp_auth_session,
        jwt_refresh_session=jwt_refresh_session,
        jwt_generator=jwt_generator,
        settings=settings,
    )


@pytest_asyncio.fixture(scope="function")
def user_logout_usecase(
    jwt_refresh_session,
):
    return CustomerLogoutUC(
        jwt_refresh_session=jwt_refresh_session,
    )


@pytest_asyncio.fixture(scope="function")
def user_google_authorization_usecase(
    transaction,
    user_repository,
    jwt_generator,
    jwt_refresh_session,
):
    return CustomerGoogleAuthorizationUC(
        transaction=transaction,
        user_repository=user_repository,
        jwt_generator=jwt_generator,
        jwt_refresh_session=jwt_refresh_session,
    )


@pytest_asyncio.fixture(scope="function")
def jwt_refresh_update_usecase(
    jwt_refresh_session,
    jwt_generator,
    user_repository,
):
    return JwtRefreshTokenUpdateUC(
        jwt_refresh_session=jwt_refresh_session,
        jwt_generator=jwt_generator,
        user_repository=user_repository,
    )