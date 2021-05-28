from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .schemas import BlogSchema
from .models import Base, BlogModel
from .database import engine, SessionLocal

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog')
def createBlog(request: BlogSchema, db: Session = Depends(get_db)):
    new_blog = BlogModel(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog')
def getAllBlog(db: Session = Depends(get_db)):
    blogs = db.query(BlogModel).all()
    return blogs


@app.get('/blog/{id}')
def getBlog(id: int, db: Session = Depends(get_db)):
    #blog = db.query(BlogModel).get(id)
    blog = db.query(BlogModel).filter(BlogModel.id == id).first()
    return blog
