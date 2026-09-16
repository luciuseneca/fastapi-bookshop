from datetime import datetime
from sqladmin import ModelView
from app.admin.column_type_formatters import datetime_format
from app.user.db.postgres.models import CustomerEventENUM, CustomerEventModel


class CustomerEventTypeFilter:
    title = "Event Type"
    parameter_name = "event_type"

    def lookups(self, request, model, run_query) -> list[tuple[str, str]]:
        return [
            (event.value, event.value.replace("_", " ").capitalize())
            for event in CustomerEventENUM
        ]

    async def get_filtered_query(self, stmt, value, model):
        if value:
            stmt = stmt.where(model.event_type == value)

        return stmt


class CustomerEventAdmin(ModelView, model=CustomerEventModel):
    name = "Customer Event"
    name_plural = "Customer Events"
    icon = "fa-solid fa-chart-line"
    identity = "user_event"

    # лог — только чтение
    can_create = False
    can_edit = False

    admin_ignored_fields = []

    column_labels = {
        CustomerEventModel.user_id: "user ID",
        CustomerEventModel.book_id: "book ID",
        CustomerEventModel.event_type: "event type",
        CustomerEventModel.category_id: "category ID",
        CustomerEventModel.author_id: "author ID",
        CustomerEventModel.metada: "metadata",
        CustomerEventModel.created_at: "created at",
        CustomerEventModel.updated_at: "updated at",
    }
    column_type_formatters = {
        datetime: datetime_format
    }

    # list
    column_list = [
        CustomerEventModel.id,
        CustomerEventModel.user_id,
        CustomerEventModel.book_id,
        CustomerEventModel.event_type,
        CustomerEventModel.weight,
        CustomerEventModel.created_at,
    ]
    column_searchable_list = [
        CustomerEventModel.id,
        CustomerEventModel.user_id,
        CustomerEventModel.book_id,
    ]
    column_sortable_list = [
        CustomerEventModel.weight,
        CustomerEventModel.created_at,
    ]
    column_filters = [CustomerEventTypeFilter()]

    page_size = 25
    page_size_options = [25, 50, 100, 200]

    # detail
    column_details_list = [
        CustomerEventModel.id,
        CustomerEventModel.user_id,
        CustomerEventModel.book_id,
        CustomerEventModel.event_type,
        CustomerEventModel.metada,
        CustomerEventModel.category_id,
        CustomerEventModel.author_id,
        CustomerEventModel.weight,
        CustomerEventModel.created_at,
        CustomerEventModel.updated_at,
    ]
