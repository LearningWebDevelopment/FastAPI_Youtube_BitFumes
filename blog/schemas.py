from typing import Optional
from pydantic import BaseModel


class BlogSchema(BaseModel):
    title: str
    body: str


class ShowBlogSchema(BlogSchema):
    class Config():
        orm_mode = True


class ShowBlogTitle(BaseModel):
    title: str
    body: str

    class Config():
        orm_mode = True


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class UserDetail(UserBase):
    id: int

    class Config():
        orm_mode = True


class UserUpdate(UserBase):
    name:  Optional[str] = None
    email:  Optional[str] = None

    class Config():
        orm_mode = True
