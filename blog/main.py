
from fastapi import FastAPI

from blog.database import Base, engine
from blog.routers import blog, user, login

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(login.router)
