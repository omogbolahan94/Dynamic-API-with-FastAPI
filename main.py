from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    message: str
    id: int


@app.get("/posts/")
async def post():
    return {"message": "Hello World"}


@app.post("/posts/")
async def post(post: Post):
    return post