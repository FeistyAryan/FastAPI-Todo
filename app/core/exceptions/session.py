from app.core.exceptions.base import CustomException

class SessionException(CustomException):
    pass

class InvalidSessionException(SessionException):
    pass
