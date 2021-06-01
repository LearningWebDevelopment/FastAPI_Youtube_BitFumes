from fastapi import HTTPException, Response, status

from blog.models import BlogModel


def get_all_blog(db):
    blogs = db.query(BlogModel).all()
    return blogs


def get_blog(id, db):
    #blog = db.query(BlogModel).get(id)
    blog = db.query(BlogModel).filter(BlogModel.id == id).all()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not Fund!!!")
        #response.status_code = status.HTTP_404_NOT_FOUND
        # return {'error': 'Blog not found!!!'}
    return blog


def create_blog(request, db):
    new_blog = BlogModel(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def delete_blog(id, db):
    blog = db.query(BlogModel).filter(
        BlogModel.id == id).delete(synchronize_session=False)
    db.commit()
    if not blog:
        raise HTTPException(
            status_code=404, detail=f"Blog {id} not found")
    # blog.delete(synchronize_session=False)
    return Response(status_code=204)


def update_blog(id, request, db):
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
