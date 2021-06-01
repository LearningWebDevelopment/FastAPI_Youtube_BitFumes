from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .schemas import BlogSchema, ShowBlogSchema, ShowBlogTitle, UserBase, UserDetail, UserCreate, UserUpdate
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
@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create_Blog(request: BlogSchema, db: Session = Depends(get_db)):
    new_blog = BlogModel(title=request.title, body=request.body, user_id=1)
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
    }, tags=['blogs']
)
def delete_Blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(BlogModel).filter(
        BlogModel.id == id).delete(synchronize_session=False)
    db.commit()
    if not blog:
        raise HTTPException(
            status_code=404, detail=f"User {id} not found")
    # blog.delete(synchronize_session=False)
    return Response(status_code=204)


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update_Blog(id: int, request: BlogSchema, db: Session = Depends(get_db)):
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


@app.get('/blog', response_model=List[ShowBlogTitle], tags=['blogs'])
def get_All_Blog(db: Session = Depends(get_db)):
    blogs = db.query(BlogModel).all()
    return blogs


@app.get('/blog/{id}', status_code=200, response_model=List[ShowBlogSchema], tags=['blogs'])
def get_Blog(id: int, response: Response, db: Session = Depends(get_db)):
    #blog = db.query(BlogModel).get(id)
    blog = db.query(BlogModel).filter(BlogModel.id == id).all()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not Fund!!!")
        #response.status_code = status.HTTP_404_NOT_FOUND
        # return {'error': 'Blog not found!!!'}
    return blog


@app.post('/user', status_code=status.HTTP_201_CREATED, response_model=UserDetail, tags=['User'])
def create_user(request: UserCreate, db: Session = Depends(get_db)):
    request.password = Hash.hash_pass(request.password)
    new_user = UserModel(**request.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/user', status_code=200, response_model=List[UserDetail], tags=['User'])
def get_all_user(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Users not Found!!!")
    return users


@app.get('/user/{id}', status_code=200, response_model=UserDetail, tags=['User'])
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).get(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not Found!!!")
    return user


@app.delete('/user/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['User'])
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


@app.patch('/user/{id}', status_code=status.HTTP_206_PARTIAL_CONTENT, response_model=UserUpdate, tags=['User'])
def partially_update_user(id: int, request: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(UserModel).get(id)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User {id} not found")

    user_model = UserBase(**vars(user))
    updated_data = request.dict(exclude_unset=True)
    updated_model = user_model.copy(update=updated_data)

    db.query(UserModel).filter(UserModel.id == id).update(
        vars(updated_model),
        synchronize_session=False)
    # blog.update(vars(request))
    db.commit()

    return updated_model


@app.put('/user/{id}', status_code=status.HTTP_205_RESET_CONTENT, response_model=UserBase, tags=['User'])
def update_user(id: int, request: UserBase, db: Session = Depends(get_db)):
    user = db.query(UserModel).get(id)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User {id} not found")

    db.query(UserModel).filter(UserModel.id == id).update(
        vars(request),
        synchronize_session=False)
    # blog.update(vars(request))
    db.commit()

    return request
