def test_hash_token():
    """
    Test that hash_token generates a valid hash and validate_token correctly verifies it.
    """
    from app.core.security.utils import hash_token, validate_token

    token = "1234qwertyZXCV"
    hashed = hash_token(token)

    assert validate_token(token=token, hashed_token=hashed) == True

def test_validate_token():
    """
    Test validate_token with a manually created bcrypt hash (SHA‑256 + bcrypt)
    and with an empty hash to ensure it returns False for invalid input.
    """

    import bcrypt
    import hashlib
    from app.core.security.utils import validate_token

    token = "My_beautiful_token_1"

    sha256_hash = hashlib.sha256(token.encode('utf-8')).digest()
    hashed_token_1 = bcrypt.hashpw(sha256_hash, bcrypt.gensalt())
    result1 = validate_token(token, hashed_token_1.decode('utf-8'))
    assert result1 is True

    hashed_token_2 = ""
    result2 = validate_token(token, hashed_token_2)
    assert result2 is False
