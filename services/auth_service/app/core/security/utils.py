import hashlib
import bcrypt



def hash_token(
        token: str,
) -> str:
    # First we'll hash all of jwt_refresh_token with SHA-256, because bcrypt can hash only 72 bytes
    sha256_hash = hashlib.sha256(token.encode('utf-8')).digest()

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(sha256_hash, salt)
    # token_bytes: bytes = sha256_hash.encode()

    return hashed.decode('utf-8')

def validate_token(
        token: str,
        hashed_token: str
) -> bool:
    sha256_hash = hashlib.sha256(token.encode('utf-8')).digest()
    return bcrypt.checkpw(sha256_hash, hashed_token.encode('utf-8'))