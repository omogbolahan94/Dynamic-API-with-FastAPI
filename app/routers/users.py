from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Optional, List
from sqlalchemy.orm import Session
from ..database import engine, get_db
from .. import models, schemas, utils


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserBase, db: Session=Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.Users(**user.dict())
     
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
