from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    id: int
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    
    class Config:
        from_attributes = True


class PostBase(BaseModel):
    id: int
    user_id: int
    created_date: datetime
    content: str
    

class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class PostResponse(PostBase):
    # what the internet returns to user
    title: str
    user: UserResponse

    class Config:
        from_attributes = True


class LoginBase(BaseModel):
    email: EmailStr  
    password: str


class Token(BaseModel):
    access_token: str  
    token_type: str


class TokenData(BaseModel):
    id: Optional[int]


class VoteBase(BaseModel):
    post_id: int  
    vote_direction: conint(le=1)


class PostWithVotes(BaseModel):
    post: PostResponse
    votes: int

    class Config:
        from_attributes = True