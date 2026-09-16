from pydantic import BaseModel

class BooksFilterSimilarREQT(BaseModel):
    book_slug: str
    category_id: int
    author_id: int