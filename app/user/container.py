from dishka import (
    Provider,
    provide,
    Scope,
)
from qdrant_client import AsyncQdrantClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.user.db.postgres.repositories.sqlalchemy import CustomerSQLAlchemyREPO
from app.user.db.postgres.repositories.sqlalchemy.customer_event import CustomerEventSQLAlchemyREPO
from app.user.db.qdrant.collections.customer_reco_profile import CustomerRecoProfileQdrantCollection
from app.user.service.infrastructure.jwt.refresh_session import JWTRefreshAuthSession
from app.user.service.infrastructure.otp.auth_session import OtpAuthSession
from app.user.db.qdrant.repositories.customer.reco_profile import CustomerRecoProfileQdrantREPO
from app.user.service.infrastructure.taskiq.schedules.customer.base import CustomerTaskiqSchedulesPublisher
from app.user.service.infrastructure.customer.reco_profile import (
    CustomerPersonalBooksRecoProfile,
    CustomerPersonalBooksRecoProfileCache,
    CustomerProfileUpdateProcess,
    CustomerRecoProfileEmbeddingTextBuilder,
)
from app.user.service.usecase.jwt.refresh_update import JwtRefreshTokenUpdateUC
from app.user.service.usecase.customer import CustomerAuthenticationUC, CustomerAuthorizationUC
from app.user.service.usecase.ouath.google_authorization import CustomerGoogleAuthorizationUC
from app.user.service.usecase.customer.logout import CustomerLogoutUC
from app.core.config.base import Settings
from app.user.service.infrastructure.jwt.generator import JWTGenerator
from app.product.db.postgres.repositories.sqlalchemy.author import BookAuthorSQLAlchemyREPO
from app.product.db.postgres.repositories.sqlalchemy.book import BookSQLAlchemyREPO
from app.product.db.postgres.repositories.sqlalchemy.category import BookCategorySQLAlchemyREPO
from app.product.db.qdrant.repositories.books import BooksQdrantREPO
from app.shared.db.postgres.repositories.sqlalchemy.transaction import SQLAlchemyTransaction
from app.shared.service.infrastructure.ollama.embedder import OllamaEmbedder
from app.shared.service.infrastructure.redis.clients import RedisClient

class ClientProvider(Provider):
    scope = Scope.REQUEST

    # ----
    #REPO

    @provide
    def user_alchemy_repo(
        self,
        session: AsyncSession,
    ) -> CustomerSQLAlchemyREPO:
        return CustomerSQLAlchemyREPO(session)
    
    @provide
    def user_event_alchemy_repo(
        self,
        session: AsyncSession,
    ) -> CustomerEventSQLAlchemyREPO:
        return CustomerEventSQLAlchemyREPO(session)
    
    # ----
    # UC
    
    @provide
    def user_authentication_uc(
        self,
        transaction: SQLAlchemyTransaction,
        user_repository: CustomerSQLAlchemyREPO,
        otp_auth_session: OtpAuthSession,
        settings: Settings,
    ) -> CustomerAuthenticationUC:
        return CustomerAuthenticationUC(
            transaction=transaction,
            user_repository=user_repository,
            otp_auth_session=otp_auth_session,
            settings=settings,
        )
    
    @provide
    def user_authorization_uc(
        self,
        transaction: SQLAlchemyTransaction,
        user_repository: CustomerSQLAlchemyREPO,
        otp_auth_session: OtpAuthSession,
        jwt_refresh_session: JWTRefreshAuthSession,
        jwt_generator: JWTGenerator,
        settings: Settings,
    ) -> CustomerAuthorizationUC:
        return CustomerAuthorizationUC(
            transaction=transaction,
            user_repository=user_repository,
            otp_auth_session=otp_auth_session,
            jwt_refresh_session=jwt_refresh_session,
            jwt_generator=jwt_generator,
            settings=settings,
        )
    
    @provide
    def user_google_authorization_uc(
        self,
        transaction: SQLAlchemyTransaction,
        user_repository: CustomerSQLAlchemyREPO,
        jwt_generator: JWTGenerator,
        jwt_refresh_session: JWTRefreshAuthSession,
    ) -> CustomerGoogleAuthorizationUC:
        return CustomerGoogleAuthorizationUC(
            transaction=transaction,
            user_repository=user_repository,
            jwt_generator=jwt_generator,
            jwt_refresh_session=jwt_refresh_session,
        )

    @provide
    def user_logout_uc(
        self,
        jwt_refresh_session: JWTRefreshAuthSession,
    ) -> CustomerLogoutUC:
        return CustomerLogoutUC(jwt_refresh_session=jwt_refresh_session)
    
    @provide
    def jwt_refresh_token_update_uc(
        self,
        jwt_refresh_session: JWTRefreshAuthSession,
        jwt_generator: JWTGenerator,
        user_repository: CustomerSQLAlchemyREPO,
    ) -> JwtRefreshTokenUpdateUC:
        return JwtRefreshTokenUpdateUC(
            jwt_generator=jwt_generator,
            jwt_refresh_session=jwt_refresh_session,
            user_repository=user_repository,
        )
    
    # ----
    # SERV
    
    @provide
    def jwt_generator(self) -> JWTGenerator:
        return JWTGenerator()
    
    @provide
    def jwt_refresh_auth_session(
        self,
        redis_connection: RedisClient,
    ) -> JWTRefreshAuthSession:
        return JWTRefreshAuthSession(redis_connection=redis_connection)
    
    @provide
    def otp_auth_session(
        self,
        redis_connection: RedisClient,
        settings: Settings,
    ) -> OtpAuthSession:
        return OtpAuthSession(
            redis=redis_connection,
            settings=settings,
        )
    
    @provide
    def user_personal_books_reco_profile_cache(
        self,
        redis: RedisClient,
    ) -> CustomerPersonalBooksRecoProfileCache:
        return CustomerPersonalBooksRecoProfileCache(redis=redis)
    
    @provide
    def user_reco_profile_qdrant_point_repo(
        self,
        qdrant_client: AsyncQdrantClient,
    ) -> CustomerRecoProfileQdrantREPO:
        return CustomerRecoProfileQdrantREPO(qdrant_client=qdrant_client)
    
    @provide
    def user_personal_books_reco_profile(
        self,
        embedder: OllamaEmbedder,
        user_profile_cache: CustomerPersonalBooksRecoProfileCache,
        user_event_repository: CustomerEventSQLAlchemyREPO,
        book_repository: BookSQLAlchemyREPO,
        book_author_repository: BookAuthorSQLAlchemyREPO,
        book_category_repository: BookCategorySQLAlchemyREPO,
        schedule_publisher: CustomerTaskiqSchedulesPublisher,
        user_reco_profile_qdrant_repo: CustomerRecoProfileQdrantREPO,
        books_qdrant_repo: BooksQdrantREPO,
        user_profile_update_locker: CustomerProfileUpdateProcess,
        user_reco_embed_text: CustomerRecoProfileEmbeddingTextBuilder,
    ) -> CustomerPersonalBooksRecoProfile:
        return CustomerPersonalBooksRecoProfile(
            embedder=embedder,
            schedule_publisher=schedule_publisher,
            user_profile_cache=user_profile_cache,
            user_event_repository = user_event_repository,
            book_repository = book_repository,
            book_author_repository = book_author_repository,
            book_category_repository = book_category_repository,
            user_reco_profile_qdrant_repo = user_reco_profile_qdrant_repo,
            books_qdrant_repo = books_qdrant_repo,
            user_profile_update_process = user_profile_update_locker,
            user_reco_embed_text=user_reco_embed_text,
        )
    
    @provide
    def user_profile_update_locker(
        self,
        redis: RedisClient,
    ) -> CustomerProfileUpdateProcess:
        return CustomerProfileUpdateProcess(redis=redis)
    
    @provide
    def user_profile_embed_text_builder(self) -> CustomerRecoProfileEmbeddingTextBuilder:
        return CustomerRecoProfileEmbeddingTextBuilder()
    
    @provide
    def user_taskiq_schedules_publisher(self) -> CustomerTaskiqSchedulesPublisher:
        return CustomerTaskiqSchedulesPublisher()
    
    @provide(scope=Scope.APP)
    def user_reco_profile_qdrant_collection(
        self,
        qdrant_client: AsyncQdrantClient,
    ) -> CustomerRecoProfileQdrantCollection:
        return CustomerRecoProfileQdrantCollection(qdrant_client=qdrant_client)
