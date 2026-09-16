from dishka import FromDishka
from fastapi import APIRouter, Depends, Response, status
from app.user.api.cookies import clear_auth_cookies, set_auth_cookies
from app.user.api.dependencies import csrf_protect, get_jwt_refresh_cookie
from app.user.api.requests.customer.auth import CustomerAuthConfirmREQT
from app.user.api.requests.customer.login import CustomerLoginREQT
from app.user.api.responses.jwt.access import JwtAccessTokenRESP
from app.user.api.requests.customer.register import CustomerRegisterREQT
from dishka.integrations.fastapi import inject
from app.user.db.qdrant.collections.customer_reco_profile import CustomerRecoProfileQdrantCollection
from app.user.service.usecase.customer.authentication import CustomerAuthenticationUC
from app.user.service.usecase.customer.authorization import CustomerAuthorizationUC
from app.user.service.usecase.customer.logout import CustomerLogoutUC
from app.user.api.responses.customer.succes_otp_send import succes_otp_sending_to_email_resp
from app.core.config.client.customer.router_urls import USER_BASE_URL_CONF, USER_LOGIN_URL_CONF, USER_LOGIN_VERIFY_URL_CONF, USER_LOGOUT_ALL_URL_CONF, USER_LOGOUT_URL_CONF, USER_REGISTER_URL_CONF, USER_REGISTER_VERIFY_URL_CONF

user_router = APIRouter(
    prefix=USER_BASE_URL_CONF,
    tags=["👨‍💻 Пользователи"],
)

@user_router.post(
    USER_REGISTER_URL_CONF,
    summary="Регистрация Пользователя",
    status_code=status.HTTP_201_CREATED,
)
@inject
async def register_user_router(
    user_data: CustomerRegisterREQT,
    user_authentication: FromDishka[CustomerAuthenticationUC],
):
    otp_session_id = await user_authentication.register(user_data)
    return succes_otp_sending_to_email_resp(otp_session_id)


@user_router.post(
    USER_LOGIN_URL_CONF,
    summary="Вход Пользователя",
    status_code=status.HTTP_200_OK,
)
@inject
async def login_user_router(
    user_data: CustomerLoginREQT,
    user_authentication: FromDishka[CustomerAuthenticationUC],
):
    otp_session_id = await user_authentication.login(user_data)
    return succes_otp_sending_to_email_resp(otp_session_id)


@user_router.post(
    USER_LOGIN_VERIFY_URL_CONF,
    summary="Подтвердить Вход",
    status_code=status.HTTP_200_OK,
)
@inject
async def user_login_confirm_router(
    user_data: CustomerAuthConfirmREQT,
    response: Response,
    user_authorization: FromDishka[CustomerAuthorizationUC],
):
    jwt = await user_authorization.login_confirm(
        user_data
    )

    set_auth_cookies(response, jwt.refresh_token)
    return JwtAccessTokenRESP(access_token=jwt.access_token)


@user_router.post(
    USER_REGISTER_VERIFY_URL_CONF,
    summary="Подтвердить Регистрацию",
    status_code=status.HTTP_200_OK,
)
@inject
async def user_register_confirm_router(
    user_data: CustomerAuthConfirmREQT,
    response: Response,
    user_authorization: FromDishka[CustomerAuthorizationUC],
):
    jwt = await user_authorization.register_confirm(
        user_data
    )

    set_auth_cookies(response, jwt.refresh_token)
    return JwtAccessTokenRESP(access_token=jwt.access_token)


@user_router.post(
    USER_LOGOUT_URL_CONF,
    summary="Выход Из Аккаунта",
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def user_logout_router(
    response: Response,
    user_logout: FromDishka[CustomerLogoutUC],
    refresh_token: str = Depends(get_jwt_refresh_cookie),
    _: None = Depends(csrf_protect),
):
    await user_logout.from_device(refresh_token)

    clear_auth_cookies(response)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@user_router.post(
    USER_LOGOUT_ALL_URL_CONF,
    summary="Выход Со Всех Устройств",
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def user_logout_all_sessions_router(
    response: Response,
    user_logout: FromDishka[CustomerLogoutUC],
    refresh_token: str = Depends(get_jwt_refresh_cookie),
    _: None = Depends(csrf_protect),
):
    await user_logout.from_all_devices(refresh_token)

    clear_auth_cookies(response)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@user_router.post("/qdrant/init/collection")
@inject
async def create_collect(user_reco_profile_qdrant_collection: FromDishka[CustomerRecoProfileQdrantCollection]):
    await user_reco_profile_qdrant_collection.init_collection()

    return {
        "status": "done"
    }