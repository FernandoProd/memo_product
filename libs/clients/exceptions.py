

class UserServiceError(Exception):
    pass

class UserServiceUnavailableError(UserServiceError):
    pass

class InvalidCredentialsError(UserServiceError):
    pass