from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str
    id: int


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class PostResponse(PostBase):
    title: str

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    id: int
    email: str
    password: str


class UserResponse:
    email: str
    
    class Config:
        from_attributes = True