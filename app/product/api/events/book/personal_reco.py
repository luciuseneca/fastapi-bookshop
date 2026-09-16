from pydantic import BaseModel, Field
from app.user.db.postgres.models import CustomerEventENUM

class BookPersonalRecoEVENT(BaseModel):
    type: CustomerEventENUM
    book_id: int | None = None
    metadata: dict = Field(default_factory=dict)


class SearchEventMeta(BaseModel):
    query: str
    results_count: int = 0


class RatingEventMeta(BaseModel):
    rating: int = Field(ge=1, le=5)