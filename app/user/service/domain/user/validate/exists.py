from app.user.db.postgres.models import UserModel

def is_user_found(user: UserModel) -> bool:
    return user is not None


def is_user_not_found(user: UserModel) -> bool:
    return user is None