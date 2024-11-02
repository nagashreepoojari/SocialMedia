from datetime import datetime, timedelta

import jwt

# secret key
# algorith
# expiration time


# import secrets
#
# def generate_secret_key(length=50):
#     return secrets.token_hex(length)
# # Example usage
# secret_key = generate_secret_key(32)
# print(secret_key)


SECRET_KEY = "1ca9cd62164baa7d5c8a28970b10232e0c6a7817fea19ba6f9c4b03492b0137d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

