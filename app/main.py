from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

database = [{"title": "We are gods","message": "We have the power to create and destroy","id": 1},
        {"title": "What us love","message": "God is love","id": 2}
]


class Post(BaseModel):
    title: str
    message: str
    id: int
    rating: Optional[int] = None


@app.get("/posts/")
async def post():
    return  {"data": database}


@app.get("/posts/{id}")
def get_post(id: int):
    
    def find_post():
        for post in database:
            if post['id'] == id:
                return post
    result = find_post()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")

    return result


@app.post("/posts/", status_code=status.HTTP_201_CREATED)
async def post(post: Post):
    database.append(post)
    return {"data": post}

