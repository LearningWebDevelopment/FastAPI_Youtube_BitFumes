from typing import List

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from blog.database import get_db
from blog.repository.blog import (create_blog, delete_blog, get_all_blog,
                                  get_blog, update_blog)
from blog.schemas import BlogSchema, ShowBlogTitle

router = APIRouter(
    prefix="/blog",
    tags=['Blogs']
)


@router.get('/', response_model=List[ShowBlogTitle])
def get_All_Blog(db: Session = Depends(get_db)):
    return get_all_blog(db)


@router.get('/{id}', status_code=200, response_model=List[ShowBlogTitle])
def get_Blog(id: int, db: Session = Depends(get_db)):
    return get_blog(id, db)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_Blog(request: BlogSchema, db: Session = Depends(get_db)):
    return create_blog(request, db)


@router.delete(
    '/{id}',
    response_class=Response,
    responses={
        204: {"description": "Blog successfully deleted"},
        404: {"description": "Topic not found"},
    }
)
def delete_Blog(id: int, db: Session = Depends(get_db)):
    return delete_blog(id, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_Blog(id: int, request: BlogSchema, db: Session = Depends(get_db)):
    return update_blog(id, request, db)
