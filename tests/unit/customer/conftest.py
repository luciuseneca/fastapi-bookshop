import pytest
from unittest.mock import AsyncMock, MagicMock, Mock
from app.core.config.client.test.dto import user_test_conf
from app.core.config.client.otp.test.dto import otp_test_conf
from app.user.service.infrastructure.otp.auth_session import OtpAuthSession
from app.user.db.postgres.models import UserRoleENUM
from app.user.db.postgres.repositories.sqlalchemy import CustomerSQLAlchemyREPO

@pytest.fixture
def fake_user_repository() -> CustomerSQLAlchemyREPO:
    fake = Mock(spec=CustomerSQLAlchemyREPO)

    fake.get_by_email_and_active = AsyncMock()
    fake.get_by_email = AsyncMock()
    fake.get_by_email_and_inactive = AsyncMock()

    return fake


@pytest.fixture
def fake_otp_repository() -> OtpAuthSession:
    fake = Mock(spec=OtpAuthSession)

    fake.get_by_owner = AsyncMock()
    fake.create = AsyncMock()

    return fake


@pytest.fixture
def fake_user():
    user = MagicMock()
    user.email = user_test_conf.email
    user.password = user_test_conf.password
    user.is_active = user_test_conf.is_active
    user.role = UserRoleENUM.CUSTOMER
    user.oauth_provider = None

    return user


@pytest.fixture
def fake_otp():
    otp = MagicMock()
    otp.owner = user_test_conf.email
    otp.code = otp_test_conf.code
    otp.ttl = otp_test_conf.ttl
    
    return otp