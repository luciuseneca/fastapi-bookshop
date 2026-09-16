
from dataclasses import dataclass

@dataclass(frozen=True)
class BookReviewOFCustomer:
    book_id: int
    user_id: int