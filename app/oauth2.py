from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
from .config import settings


def create_access_token(data: dict):
    # data is an id key value pair values
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=int(settings.jwt_access_token_expire_minutes))
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload  #{'user_id': user.id}


def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="login"))):
    user = verify_access_token(token) 
    return user.get('user_id')
