from abc import ABC, abstractmethod
from app.user.service.infrastructure.taskiq.schedules.customer.update_customer_recs_vector import update_user_reco_books_profile_schedule
from app.core.config.user.customer.personal_book_reco import VECTOR_UPDATE_DELAY

class ICustomerSchedulesPublisher(ABC):
    @abstractmethod
    async def update_user_reco_profile(self, user_id: int) -> None:
        pass


class CustomerTaskiqSchedulesPublisher(ICustomerSchedulesPublisher):
    async def update_user_reco_profile(self, user_id: int) -> None:
        await (
            update_user_reco_books_profile_schedule.kicker().with_labels(
                delay=VECTOR_UPDATE_DELAY
            ).kiq(user_id)
        )