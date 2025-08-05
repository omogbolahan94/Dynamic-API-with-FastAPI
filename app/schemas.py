from pydantic import BaseModel, EmailStr
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    id: int


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class PostResponse(BaseModel):
    # what the internet returns to user
    id: int
    title: str

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    id: int
    email: str  # EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str  # EmailStr
    
    class Config:
        from_attributes = True


class LoginBase(BaseModel):
    email: str  
    password: str


class TokenBase(BaseModel):
    acces_token: str  
    token_type: str


class TokenBase(BaseModel):
    id: Optional[int]