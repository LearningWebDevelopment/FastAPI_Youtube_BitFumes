

from pydantic import BaseModel


class BlogSchema(BaseModel):
    title: str
    body: str


class ShowBlogSchema(BlogSchema):
    class Config():
        orm_mode = True
