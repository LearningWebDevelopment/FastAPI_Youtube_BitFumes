from typing import List, Optional

from pydantic import BaseModel


class BlogSchema(BaseModel):
    title: str
    body: str

    class Config():
        orm_mode = True


class UserBase(BaseModel):
    name: str
    email: str

    class Config():
        orm_mode = True


class UserCreate(UserBase):
    password: str


class UserDetail(UserBase):
    id: int
    blogs: List[BlogSchema] = []

    class Config():
        orm_mode = True


class UserUpdate(UserBase):
    name:  Optional[str] = None
    email:  Optional[str] = None

    class Config():
        orm_mode = True


class ShowBlogTitle(BaseModel):
    title: str
    body: str
    author: UserBase

    class Config():
        orm_mode = True


class ShowBlogSchema(BlogSchema):
    author: UserDetail

    class Config():
        orm_mode = True


class LoginSchema(BaseModel):
    username:  str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
