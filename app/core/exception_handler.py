from fastapi import Request
from fastapi.responses import JSONResponse
from app.shared.exception import AppException

async def exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Convert an application exception into a JSON error response.

    Preserve the exception's HTTP status and expose its message as the detail
    field. The response is serialized directly without a response model.

    Args:
        request: Request that triggered the exception.
        exc: Application exception containing the status code and message.

    Returns:
        JSON response containing the error detail and configured status code.
    """
    return JSONResponse(
        status_code=exc.code,
        content={"detail": exc.msg},
    )