

from fastapi import HTTPException, status

from blog.hashing import Hash
from blog.models import UserModel
from blog.schemas import UserBase


def get_all_user(db):
    users = db.query(UserModel).all()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Users not Found!!!")
    return users


def get_user(id, db):
    user = db.query(UserModel).get(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not Found!!!")
    return user


def create_user(request, db):
    request.password = Hash.hash_pass(request.password)
    new_user = UserModel(**request.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def delete_user(id, db):
    user = db.query(UserModel).filter(
        UserModel.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not Found!!!")
    db.query(UserModel).filter(UserModel.id ==
                               id).delete(synchronize_session=False)
    db.commit()
    return {'detail': 'User Destroyed'}


def partially_update_user(id, request, db):
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


def update_user(id, request, db):
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
