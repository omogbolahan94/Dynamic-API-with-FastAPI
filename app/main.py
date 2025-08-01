from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
import psycopg2

app = FastAPI()


database = [{"title": "We are gods","message": "We have the power to create and destroy","id": 1},
        {"title": "What us love","message": "God is love","id": 2}
]


class Post(BaseModel):
    title: str
    message: str
    id: int
    # rating: Optional[int] = None

# set upconnection to database
try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="Post_DB",
        user="postgres",
        password="postgres"
    )
except psycopg2.Error as error:
    print(f"Error!!! {error}")
else:
    cur = conn.cursor()
    


@app.get("/posts/")
async def post():
    cur.execute("SELECT * FROM posts")
    posts = cur.fetchall()
    
    return  {"data": posts}


@app.get("/posts/{id}")
def get_post(id: int):
    
    cur.execute("SELECT * FROM posts WHERE id=%s", str(id))
    post = cur.fetchone()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id '{id}' was not found")

    return post


@app.post("/posts/", status_code=status.HTTP_201_CREATED)
async def post(post: Post):
    try:
        cur.execute("INSERT INTO posts (title, content, id) VALUES (%s, %s, %s) RETURNING *", 
                    (post.title, post.message, post.id) )
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{error}")
    else:
        new_post = cur.fetchone()
    
    conn.commit()
    # cur.close()
    
    return {"data": new_post} 


@app.put("/posts/{id}")
def update_post(id:int, post: Post):
    cur.execute("UPDATE posts SET title=%s, content=%s WHERE id=%s RETURNING *", 
                    (post.title, post.message, str(id)) )

    updated_post = cur.fetchone()
    conn.commit()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id '{id}' was not found")

    return updated_post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cur.execute("DELETE FROM posts WHERE id=%s RETURNING *", (str(id)) )

    deleted_post = cur.fetchone()
    conn.commit()

    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id '{id}' was not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)





