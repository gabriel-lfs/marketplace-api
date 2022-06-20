from typing import Optional

from fastapi import status, FastAPI
from fastapi.responses import ORJSONResponse
from starlette.requests import Request


class APIError(Exception):
    def __init__(self, status_code: Optional[int] = None, message: Optional[str] = None, data: Optional[dict] = None):
        self.status_code = status_code or status.HTTP_500_INTERNAL_SERVER_ERROR
        self.message = message or 'Unexpected error'
        self.data = data or {}


def setup_exception_handlers(app: FastAPI):
    def api_error_handler(request: Request, exc: APIError):
        return ORJSONResponse(
            {
                "message": exc.message,
                "data": exc.data
            },
            status_code=exc.status_code
        )

    app.add_exception_handler(APIError, api_error_handler)