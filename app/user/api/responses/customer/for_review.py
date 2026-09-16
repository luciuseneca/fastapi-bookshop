from pydantic import BaseModel

class CustomerReviewPreviewRESP(BaseModel):
    id: int
    email: str
    username: str

    model_config = {
        "from_attributes": True
    }