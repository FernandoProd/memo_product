class UserServiceError(Exception):
    """ Basic except for user_service errors"""
    pass

class UserServiceUnavailableError(UserServiceError):
    pass

class InvalidCredentialsError(UserServiceError):
    pass