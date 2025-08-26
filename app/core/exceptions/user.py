from app.core.exceptions.base import CustomException

class UserException(CustomException):
    pass

class UserAlreadyExistsException(UserException):
    pass

class UserNotFoundException(UserException):
    pass

class InvalidCredentialsException(UserException):
    def __init__(self, detail: str = "Could not validate credentials, please log in again."):
        self.detail = detail