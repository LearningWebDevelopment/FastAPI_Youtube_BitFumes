"""
Created to learn FastAPI
"""

from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

# Create instance of FastAPI
app = FastAPI()


class Blog(BaseModel):
    title: str
    body: str
    published : Optional[bool]


@app.get('/blog')
def index(limit: int = 10, published: bool = False, sort: Optional[str] = None):
    if published:
        return {'data': 'Published Blogs only'}
    elif limit:
        return {'data': f'Blog List Limited to {limit}'}


@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'unpublished blog list'}


@app.get('/blog/{id}')
def show(id: int):
    return {'data': id}


@app.get('/blog/{id}/comments')
def comments(id):
    return {'data': {'1': 'comment 1', '2': 'comment 2'}}


@app.post('/blog')
def create_blog(request_blog: Blog):
    return {'data': f'Blog is Created with title {request_blog.title}'}
