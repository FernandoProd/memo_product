import bcrypt
import logging


logger = logging.getLogger(__name__)


def hash_password(
        password: str,
) -> bytes:
    """
    Hash a plain text password using bcrypt
    """

    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()

    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(
        password: str,
        hashed_password: str,
) -> bool:
    """
    Verify a password against its bcrypt hash
    """

    try:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )
    except ValueError as e:
        logger.error("Invalid bcrypt hash provided: %s", e)
        return False
