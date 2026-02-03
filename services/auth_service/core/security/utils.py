import bcrypt


def hash_token(
        token: str,
) -> bytes:
    salt = bcrypt.gensalt()
    token_bytes: bytes = token.encode()

    return bcrypt.hashpw(token_bytes, salt)

def validate_token(
        token: str,
        hashed_token: str,
) -> bool:
    return bcrypt.checkpw(
        password=token.encode('utf-8'),
        hashed_password=hashed_token.encode('utf-8'),  # str -> bytes
    )