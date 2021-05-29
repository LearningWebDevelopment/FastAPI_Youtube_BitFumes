from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .schemas import BlogSchema, ShowBlogSchema, ShowBlogTitle, UserDetail, UserCreate
from .models import Base, BlogModel, UserModel
from .database import engine, SessionLocal
from .hashing import Hash

app = FastAPI()

Base.metadata.create_all(bind=engine)


class Status(BaseModel):
    message: str


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


@app.delete(
    '/blog/{id}',
    response_class=Response,
    responses={
        204: {"description": "Blog successfully deleted"},
        404: {"description": "Topic not found"},
    },
)
def deleteBlog(id: int, db: Session = Depends(get_db)):
    blog = db.query(BlogModel).filter(
        BlogModel.id == id).delete(synchronize_session=False)
    db.commit()
    if not blog:
        raise HTTPException(
            status_code=404, detail=f"User {id} not found")
    # blog.delete(synchronize_session=False)
    return Response(status_code=204)


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def updateBlog(id: int, request: BlogSchema, db: Session = Depends(get_db)):
    #blog = db.query(BlogModel).filter(BlogModel.id == id)
    blog = db.query(BlogModel).get(id)
    if not blog:
        raise HTTPException(
            status_code=404, detail=f"User {id} not found")

    # blog = db.query(BlogModel).filter(BlogModel.id == id).update(
    #    {'title': request.title, 'body': request.body},
    #    synchronize_session=False)
    db.query(BlogModel).filter(BlogModel.id == id).update(
        vars(request),
        synchronize_session=False)
    # blog.update(vars(request))
    db.commit()

    return f"Blog {id} Updated"


@app.get('/blog', response_model=List[ShowBlogTitle])
def getAllBlog(db: Session = Depends(get_db)):
    blogs = db.query(BlogModel).all()
    return blogs


@app.get('/blog/{id}', status_code=200, response_model=ShowBlogSchema)
def getBlog(id: int, response: Response, db: Session = Depends(get_db)):
    #blog = db.query(BlogModel).get(id)
    blog = db.query(BlogModel).filter(BlogModel.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not Fund!!!")
        #response.status_code = status.HTTP_404_NOT_FOUND
        # return {'error': 'Blog not found!!!'}
    return blog


@app.post('/user', status_code=status.HTTP_201_CREATED, response_model=UserDetail)
def create_user(request: UserCreate, db: Session = Depends(get_db)):
    request.password = Hash.hash_pass(request.password)
    new_user = UserModel(**request.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/user', status_code=200, response_model=List[UserDetail])
def get_all_user(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Users not Found!!!")
    return users


@app.get('/user/{id}', status_code=200, response_model=UserDetail)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).get(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not Found!!!")
    return user


@app.delete('/user/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(
        UserModel.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not Found!!!")
    db.query(UserModel).filter(UserModel.id ==
                               id).delete(synchronize_session=False)
    db.commit()
    return {'detail': 'User Destroyed'}
