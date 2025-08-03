from pydantic import BaseModel


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
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    
    class Config:
        from_attributes = True