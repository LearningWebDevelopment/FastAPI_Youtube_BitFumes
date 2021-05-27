"""
Created to learn FastAPI
"""

from typing import Optional
from fastapi import FastAPI

# Create instance of FastAPI
app = FastAPI()


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
