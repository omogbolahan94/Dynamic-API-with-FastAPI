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


class UserTestResponse(BaseModel):
    password: str
    email: EmailStr
    
    class Config:
        from_attributes = True



class PostBase(BaseModel):
    id: int
    title: str
    content: str
    created_date: datetime
    published: bool

class PostCreate(BaseModel):
    title: str       
    content: str  
    published: bool = True 


class PostUpdate(PostBase):
    pass


class PostResponse(PostBase):
    # what the internet returns to user after posting
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