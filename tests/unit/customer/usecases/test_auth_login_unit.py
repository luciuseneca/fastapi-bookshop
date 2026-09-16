import pytest
from unittest.mock import AsyncMock, patch

from app.user.exception.otp.expire import OtpNotExpiredERR
from app.user.exception.customer.invalid_creds import CustomerInvalidCredentialsERR

@pytest.mark.asyncio
async def test_login_success(
    user_authentication_usecase,
    fake_user_repository,
    fake_otp_repository,
    fake_user,
    user_login_reqt,
):
    fake_user_repository.get_by_email_and_active.return_value = fake_user
    fake_otp_repository.get_by_owner.return_value = None

    with patch(
        "app.user.service.usecase.customer.authentication.user_check_password",
        return_value=True,
    ), patch(
        "app.user.service.usecase.customer.authentication.generate_otp",
        return_value="123456",
    ), patch(
        "app.user.service.usecase.customer.authentication.send_otp_email.kiq",
        new_callable=AsyncMock,
    ) as mock_send_email:
        await user_authentication_usecase.login(user_login_reqt)

        fake_otp_repository.create.assert_awaited_once()
        mock_send_email.assert_awaited_once_with(
            user_login_reqt.email,
            "123456",
        )


@pytest.mark.asyncio
async def test_login_user_not_found(
    user_authentication_usecase,
    fake_user_repository,
    user_login_reqt,
):
    fake_user_repository.get_by_email_and_active.return_value = None

    with pytest.raises(CustomerInvalidCredentialsERR):
        await user_authentication_usecase.login(user_login_reqt)


@pytest.mark.asyncio
async def test_login_otp_not_expired(
    user_authentication_usecase,
    fake_user_repository,
    fake_otp_repository,
    fake_user,
    fake_otp,
    user_login_reqt,
):
    fake_user_repository.get_by_email_and_active.return_value = fake_user
    fake_otp_repository.get_by_owner.return_value = fake_otp

    with patch(
        "app.user.service.usecase.customer.authentication.user_check_password",
        return_value=True,
    ):
        with pytest.raises(OtpNotExpiredERR):
            await user_authentication_usecase.login(user_login_reqt)