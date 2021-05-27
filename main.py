"""
Created to learn FastAPI
"""

from fastapi import FastAPI

# Create instance of FastAPI
app = FastAPI()


@app.get('/')
def index():
    return {'data': 'Blog List'}


@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'unpublished blog list'}


@app.get('/blog/{id}')
def show(id: int):
    return {'data': id}


@app.get('/blog/{id}/comments')
def comments(id):
    return {'data': {'1': 'comment 1', '2': 'comment 2'}}
