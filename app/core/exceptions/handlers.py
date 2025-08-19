from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from .base import CustomException
from .user import UserAlreadyExistsException, UserNotFoundException, InvalidCredentialsException
from .session import InvalidSessionException

async def custom_exception_handler(request: Request, exc: CustomException):
    status_code = 500
    detail = "An unexpected server error occurred."
    headers = {}

    if isinstance(exc, UserAlreadyExistsException):
        status_code = HTTP_409_CONFLICT
        detail = "A user with this email already exists."
    elif isinstance(exc, UserNotFoundException):
        status_code = HTTP_404_NOT_FOUND
        detail = "User not found."
    elif isinstance(exc, (InvalidCredentialsException, InvalidSessionException)):
        status_code = HTTP_401_UNAUTHORIZED
        detail = "Could not validate credentials, please log in again."
        headers = {"WWW-Authenticate": "Bearer"}
    
    return JSONResponse(status_code=status_code, content={"detail": detail}, headers=headers)