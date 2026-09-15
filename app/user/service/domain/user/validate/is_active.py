from app.user.db.postgres.models import UserModel

def is_user_active(user: UserModel) -> bool:
    return user.is_active


def is_user_not_active(user: UserModel) -> bool:
    return not user.is_active