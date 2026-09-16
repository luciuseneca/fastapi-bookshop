import pytest
from unittest.mock import AsyncMock, Mock
from app.user.api.requests.customer.login import CustomerLoginREQT
from app.user.service.usecase.customer.authentication import CustomerAuthenticationUC
from app.core.config.user.test.dto import user_test_conf

@pytest.fixture
def user_authentication_usecase(fake_user_repository, fake_otp_repository):
    return CustomerAuthenticationUC(
        transaction=AsyncMock(),
        settings=Mock(otp=Mock(ttl=300)),
        user_repository=fake_user_repository,
        otp_auth_session=fake_otp_repository,
    )


@pytest.fixture
def user_login_reqt():
    return CustomerLoginREQT(
        email=user_test_conf.email,
        password=user_test_conf.password,
    )