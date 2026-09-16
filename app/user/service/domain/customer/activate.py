from __future__ import annotations
from datetime import datetime, timezone
from app.user.db.postgres.models import UserModel

def user_make_active(user: UserModel) -> None:
    user.is_active = True
    user.created_at = datetime.now(timezone.utc)