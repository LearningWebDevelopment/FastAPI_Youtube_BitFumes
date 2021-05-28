from fastapi import FastAPI

from .schemas import Blog
from .models import Base
from .database import engine

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.post('/blog')
def create(request: Blog):
    return request
