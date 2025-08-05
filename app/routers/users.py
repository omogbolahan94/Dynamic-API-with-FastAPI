from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Optional, List
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, utils


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserBase, db: Session=Depends(get_db)):

    user_exist = db.query(models.Users).filter(models.Users.id ==user.id).first()
    
    if user_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User id '{user.id}' already exist")

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.Users(**user.dict())
     
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/", response_model=List[schemas.UserResponse])
def post(db: Session = Depends(get_db)):
    users = db.query(models.Users).all()
    return users  