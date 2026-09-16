from app.user.api.requests.customer.auth import CustomerAuthorizedREQT
from app.user.db.postgres.repositories.sqlalchemy import CustomerSQLAlchemyREPO
from app.user.exception.customer.invalid_creds import CustomerInvalidCredentialsERR
from app.product.db.postgres.models.review import ReviewModel
from app.product.db.postgres.repositories.sqlalchemy.book import BookSQLAlchemyREPO
from app.product.db.postgres.repositories.sqlalchemy.review import BookReviewSQLAlchemyREPO
from app.product.dto.review.filter_by_customer_and_book import BookReviewOFCustomer
from app.product.exceptions import BookNotFoundERR, BookReviewAlreadyExistsERR
from app.product.service.domain.book.set_avg_rating import book_avg_rating
from app.shared.service.infrastructure.base import is_exists
from app.shared.db.postgres.repositories.sqlalchemy.transaction import SQLAlchemyTransaction
from app.product.api.requests.review.write import ReviewWriteREQT

class WriteReview:
    def __init__(self,
        transaction: SQLAlchemyTransaction,
        review_repository: BookReviewSQLAlchemyREPO,
        user_repository: CustomerSQLAlchemyREPO,
        book_repository: BookSQLAlchemyREPO,
    ):
        self._transaction = transaction
        self.review_repository = review_repository
        self.user_repository = user_repository
        self.book_repository = book_repository
        
    async def for_book(
        self,
        user: CustomerAuthorizedREQT,
        review_data: ReviewWriteREQT
    ) -> None:
        user = await is_exists(
            self.user_repository.get_by_id(user.sub),
            CustomerInvalidCredentialsERR(),
        )

        book = await is_exists(
            self.book_repository.get_by_id(id=review_data.book_id),
            BookNotFoundERR(),
        )

        user_book_review_data = BookReviewOFCustomer(
            book_id=review_data.book_id,
            user_id=user.id,
        )
        review_is_exists = await self.review_repository.get_by_book_and_user_id(user_book_review_data)

        if review_is_exists:
            raise BookReviewAlreadyExistsERR()
        
        new_review = ReviewModel(
            user_id=user.id,
            book_id=book.id,
            rating=review_data.rating,
            comment=review_data.comment,
        )
        await self.review_repository.save(new_review)

        book_avg_rating(
            book=book,
            rating=review_data.rating,
        )
        await self.book_repository.save(book)

        await self._transaction.commit()