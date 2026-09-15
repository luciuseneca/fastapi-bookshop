from app.user.db.postgres.models import UserModel

def user_update_credentials(
    user: UserModel,
    password: str,
    username: str,
    user_role: str,
) -> None:
    user.password = password
    user.username = username
    user.role = user_role