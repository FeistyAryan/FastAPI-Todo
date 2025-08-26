from app.core.exceptions.base import CustomException

class SessionException(CustomException):
    pass

class InvalidSessionException(SessionException):
    def __init__(self, detail: str = "Could not validate credentials, please log in again."):
        self.detail = detail
