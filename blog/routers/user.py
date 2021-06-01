from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from blog.database import get_db
from blog.repository import user
from blog.schemas import UserBase, UserCreate, UserDetail, UserUpdate

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)


@router.get('/', status_code=200, response_model=List[UserDetail])
def get_all_user(db: Session = Depends(get_db)):
    return user.get_all_user(db)


@router.get('/{id}', status_code=200, response_model=UserDetail)
def get_user(id: int, db: Session = Depends(get_db)):
    return user.get_user(id, db)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserDetail)
def create_user(request: UserCreate, db: Session = Depends(get_db)):
    return user.create_user(request, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    return user.delete_user(id, db)


@router.patch('/{id}', status_code=status.HTTP_206_PARTIAL_CONTENT, response_model=UserUpdate)
def partially_update_user(id: int, request: UserUpdate, db: Session = Depends(get_db)):
    return user.partially_update_user(id, request, db)


@router.put('/{id}', status_code=status.HTTP_205_RESET_CONTENT, response_model=UserBase)
def update_user(id: int, request: UserBase, db: Session = Depends(get_db)):
    return user.update_user(id, request, db)
