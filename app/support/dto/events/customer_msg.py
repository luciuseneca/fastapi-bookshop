from pydantic import BaseModel

class ChatCustomerMsgEVT(BaseModel):
    model_config = {"frozen": True}

    chat_id: int
    message: str
