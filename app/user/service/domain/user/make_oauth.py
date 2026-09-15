from app.user.db.postgres.models import UserModel, OAuthProviderENUM

def user_make_is_google(user: UserModel, oauth_id: str) -> None:
    user.oauth_provider = OAuthProviderENUM.GOOGLE
    user.oauth_id = oauth_id