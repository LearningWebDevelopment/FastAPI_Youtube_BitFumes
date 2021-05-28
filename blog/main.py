from fastapi import FastAPI, Depends, status, Response, HTTPException
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


# @app.post('/blog', status_code=201)
@app.post('/blog', status_code=status.HTTP_201_CREATED)
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


@app.get('/blog/{id}', status_code=200)
def getBlog(id: int, response: Response, db: Session = Depends(get_db)):
    #blog = db.query(BlogModel).get(id)
    blog = db.query(BlogModel).filter(BlogModel.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not Fund!!!")
        #response.status_code = status.HTTP_404_NOT_FOUND
        # return {'error': 'Blog not found!!!'}
    return blog
