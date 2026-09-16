import pytest
from app.user.api.requests.customer.google_oauth import CustomerOauthREQT
from app.user.api.requests.customer.login import CustomerLoginREQT
from app.user.api.requests.customer.register import CustomerRegisterREQT
from app.core.config.client.test.dto import user_test_conf, user_google_test_conf

# client
@pytest.fixture
def user_login_reqt():
    return CustomerLoginREQT(
        email=user_test_conf.email,
        password=user_test_conf.password,
    )


@pytest.fixture
def user_register_reqt():
    return CustomerRegisterREQT(
        email=user_test_conf.email,
        username=user_test_conf.username,
        password=user_test_conf.password,
    )


@pytest.fixture
def user_google_reqt():
    return CustomerOauthREQT(
        email=user_google_test_conf.email,
        username=user_google_test_conf.username,
        oauth_id=user_google_test_conf.oauth_id,
    )