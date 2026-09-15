from app.user.db.postgres.models import UserModel, OAuthProviderENUM

def is_google_user(user: UserModel) -> bool:
    return user.oauth_provider == OAuthProviderENUM.GOOGLE


def is_invalid_google_account(user: UserModel, oauth_id: str) -> bool:
    return user.oauth_id != oauth_id