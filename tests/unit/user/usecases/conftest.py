import pytest
from unittest.mock import AsyncMock, Mock
from app.user.api.requests.user.login import UserLoginREQT
from app.user.service.usecase.user.authentication import UserAuthenticationUC
from app.core.config.client.test.dto import user_test_conf

@pytest.fixture
def user_authentication_usecase(fake_user_repository, fake_otp_repository):
    return UserAuthenticationUC(
        transaction=AsyncMock(),
        settings=Mock(otp=Mock(ttl=300)),
        user_repository=fake_user_repository,
        otp_auth_session=fake_otp_repository,
    )


@pytest.fixture
def user_login_reqt():
    return UserLoginREQT(
        email=user_test_conf.email,
        password=user_test_conf.password,
    )