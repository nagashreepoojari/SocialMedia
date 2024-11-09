from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    password: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    votes: int

    # owner: UserBase

    class Config:
        from_attributes = True


class Login(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class Vote(BaseModel):
    post_id: int
    dir: int
