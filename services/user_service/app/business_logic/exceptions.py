class DuplicateEmailError(Exception):
    """Raised when trying to create a user with an existing email"""
    pass