

from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session

from blog.database import get_db
from blog.hashing import Hash
from blog.models import UserModel
from blog.schemas import LoginSchema, UserDetail
from blog.token import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token

router = APIRouter(
    prefix="/login",
    tags=['Login']
)


@router.post('/')
def login(request: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(
        UserModel.email == request.username).first()
    if not user:
        raise HTTPException(
            status_code=404, detail=f"Invalid Credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
