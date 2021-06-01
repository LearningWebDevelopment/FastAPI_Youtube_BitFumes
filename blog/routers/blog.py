from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from blog.database import get_db
from blog.models import BlogModel
from blog.schemas import BlogSchema, ShowBlogSchema, ShowBlogTitle

router = APIRouter(
    prefix="/blog",
    tags=['Blogs']
)


@router.get('/', response_model=List[ShowBlogTitle])
def get_All_Blog(db: Session = Depends(get_db)):
    blogs = db.query(BlogModel).all()
    return blogs


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_Blog(request: BlogSchema, db: Session = Depends(get_db)):
    new_blog = BlogModel(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.delete(
    '/{id}',
    response_class=Response,
    responses={
        204: {"description": "Blog successfully deleted"},
        404: {"description": "Topic not found"},
    }
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


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
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


@router.get('/{id}', status_code=200, response_model=List[ShowBlogTitle])
def get_Blog(id: int, response: Response, db: Session = Depends(get_db)):
    #blog = db.query(BlogModel).get(id)
    blog = db.query(BlogModel).filter(BlogModel.id == id).all()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not Fund!!!")
        #response.status_code = status.HTTP_404_NOT_FOUND
        # return {'error': 'Blog not found!!!'}
    return blog
