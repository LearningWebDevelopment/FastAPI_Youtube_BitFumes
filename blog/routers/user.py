from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from blog.database import get_db
from blog.hashing import Hash
from blog.models import UserModel
from blog.schemas import UserBase, UserCreate, UserDetail, UserUpdate

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserDetail)
def create_user(request: UserCreate, db: Session = Depends(get_db)):
    request.password = Hash.hash_pass(request.password)
    new_user = UserModel(**request.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/', status_code=200, response_model=List[UserDetail])
def get_all_user(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Users not Found!!!")
    return users


@router.get('/{id}', status_code=200, response_model=UserDetail)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).get(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not Found!!!")
    return user


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
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


@router.patch('/{id}', status_code=status.HTTP_206_PARTIAL_CONTENT, response_model=UserUpdate)
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


@router.put('/{id}', status_code=status.HTTP_205_RESET_CONTENT, response_model=UserBase)
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
