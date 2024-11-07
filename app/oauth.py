from datetime import datetime, timedelta
from http.client import HTTPException

import jwt
from .models import User
from .config import settings
from .schemas import UserBase, UserResponse

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


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


class CredentialException(Exception):
    def __init__(self, message="Invalid or expired token"):
        self.message = message
        super().__init__(self.message)


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get('user_id')
        if id is None:
            raise CredentialException()
        return payload
    except jwt.ExpiredSignatureError:
        raise CredentialException("Token has expired")
    except jwt.InvalidTokenError:
        raise CredentialException("Invalid token")
    except Exception as e:
        raise CredentialException(f"An error occurred: {str(e)}")


def get_current_user(token):
    token = verify_access_token(token)
    current_user = User.query.get(token.get('user_id'))

    return current_user

