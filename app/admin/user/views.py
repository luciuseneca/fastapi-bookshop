from datetime import datetime
from sqladmin import ModelView
from sqladmin.filters import BooleanFilter, OperationColumnFilter
from app.admin.user.filters import UserRoleFilterAdmin, OauthProviderFilterAdmin
from app.admin.column_type_formatters import datetime_format
from app.user.db.postgres.models import UserModel

class UserAdmin(ModelView, model=UserModel):
    """Manage user accounts in the admin interface.

    Configure the displayed fields, role filters, and editable account
    attributes for the user model.
    """

    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"
    identity = "user"

    column_labels = {
        UserModel.is_active: "is active",
        UserModel.role: "role",
        UserModel.created_at: "created at",
        UserModel.updated_at: "updated at"
    }
    column_type_formatters = {
        datetime: datetime_format
    }

    # list
    column_list = [
        UserModel.id,
        UserModel.email,
        UserModel.username,
        UserModel.oauth_provider,
        UserModel.is_active,
        UserModel.role,
        UserModel.created_at,
        UserModel.updated_at,
    ]
    column_formatters = {
        UserModel.username: lambda m, a: m.username[:10] if m.username else ""
    }
    column_searchable_list = [UserModel.id, UserModel.email]
    column_sortable_list = [UserModel.id, UserModel.created_at]
    column_filters = [
        OauthProviderFilterAdmin(),
        UserRoleFilterAdmin(),
        BooleanFilter(UserModel.is_active),
        OperationColumnFilter(UserModel.email),
    ]
    
    page_size = 25
    page_size_options = [25, 50, 100, 200]

    # detail
    column_details_list = [
        UserModel.id,
        UserModel.email,
        UserModel.username,
        UserModel.is_active,
        UserModel.role,
        UserModel.oauth_provider,
        UserModel.oauth_id,
        UserModel.created_at,
        UserModel.updated_at,
    ]

    # form
    form_columns = [
        UserModel.email,
        UserModel.username,
        UserModel.password,
        UserModel.role,
        UserModel.is_active,
        UserModel.reviews
    ]
    form_ajax_refs = {
        "reviews": {
            "fields": ("id",),
            "order_by": "id",
        }
    }

    form_create_rules = [
        "email",
        "username",
        "password",
        "role",
        "is_active",
    ]
    form_edit_rules = [
        "username",
        "role",
        "is_active",
    ]