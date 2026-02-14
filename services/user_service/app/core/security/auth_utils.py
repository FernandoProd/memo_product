import bcrypt



def hash_password(
        password: str,
) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()

    return bcrypt.hashpw(pwd_bytes, salt)

def validate_password(
        password: str,
        hashed_password: str,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode('utf-8'),
        hashed_password=hashed_password.encode('utf-8'),  # str -> bytes
    )



    # return bcrypt.checkpw(
    #     password=password.encode(),
    #     hashed_password=hashed_password,
    # )