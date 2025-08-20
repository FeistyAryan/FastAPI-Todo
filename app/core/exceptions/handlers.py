import structlog
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from app.core.context import request_id_var
from app.core.exceptions.base import CustomException
from app.core.exceptions.user import UserAlreadyExistsException, UserNotFoundException, InvalidCredentialsException
from app.core.exceptions.session import InvalidSessionException

log = structlog.get_logger()

async def generic_exception_handler(request: Request, exc: Exception):
    log.exception("unhandled_application_error", exc_info=exc, request_id=str(request_id_var.get()))
    return JSONResponse(status_code=500, content={"detail": "An internal server error occurred."},)

async def custom_exception_handler(request: Request, exc: CustomException):
    status_code = 500
    detail = "An unexpected server error occurred."
    headers = {}

    if isinstance(exc, UserAlreadyExistsException):
        status_code = HTTP_409_CONFLICT
        detail = "A user with this email already exists."
        log.warn("user_creation_failed_due_to_duplicate_email", exception=exc.__class__.__name__, request_id=str(request_id_var.get()))

    elif isinstance(exc, UserNotFoundException):
        status_code = HTTP_404_NOT_FOUND
        detail = "User not found."
        log.warn("user_not_found", exception=exc.__class__.__name__, request_id=str(request_id_var.get()))

    elif isinstance(exc, (InvalidCredentialsException, InvalidSessionException)):
        status_code = HTTP_401_UNAUTHORIZED
        detail = "Could not validate credentials, please log in again."
        headers = {"WWW-Authenticate": "Bearer"}
        log.warn("authentication_failed", exception=exc.__class__.__name__, request_id=str(request_id_var.get()))
    
    return JSONResponse(status_code=status_code, content={"detail": detail}, headers=headers)