from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends
from sse_starlette.sse import EventSourceResponse

from app.agents.api.requests import AgentChatREQT
from app.agents.service import AgentChatService
from app.user.api.dependencies import auth_client
from app.user.api.requests.customer.auth import CustomerAuthorizedREQT

agent_router = APIRouter(prefix="/agent", tags=["🤖 ИИ Консультант"])


@agent_router.post(
    "/chat",
    summary="Чат с ИИ агентом-консультантом (SSE)",
)
@inject
async def agent_chat_router(
    body: AgentChatREQT,
    service: FromDishka[AgentChatService],
    user: CustomerAuthorizedREQT = Depends(auth_client),
):
    """SSE-события: `token` (кусок текста), `tool` (вызов инструмента),
    `done` (полный ответ), `error`."""
    return EventSourceResponse(
        service.stream_chat(
            user_id=user.sub,
            message=body.message,
        ),
    )
