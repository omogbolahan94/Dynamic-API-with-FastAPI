from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, utils


router = APIRouter(tags=["Authentication"])


@router.post('/login')
def login(user_credentials: schemas.LoginBase, db: Session=Depends(get_db)):
    # since email is unique for all users
    user = db.query(models.Users).filter(models.Users.email == user_credentials.email).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid credentials")


    # create and return token
    return {"Token": 'example token'}
