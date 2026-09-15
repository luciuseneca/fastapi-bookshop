from app.user.db.postgres.models import UserModel

def is_not_oauth_user(user: UserModel) -> bool:
    return user.oauth_provider is None