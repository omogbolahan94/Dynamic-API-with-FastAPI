from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from pathlib import Path


# env_path = Path(os.getcwd()).resolve().parents[0] / '.env'
# load_dotenv(dotenv_path=env_path, override=True)

load_dotenv(override=True)

app = FastAPI()


class Post(BaseModel):
    title: str
    message: str
    id: int
    # rating: Optional[int] = None

hostname = os.getenv('HOST')
port = os.getenv('PORT')
db = os.getenv('DB_NAME')
user = os.getenv('USER')
password = os.getenv('PASSWORD')
# print(hostname, port, db, user, password)

try:
    conn = psycopg2.connect(
        host=hostname,
        port=port,
        dbname=db,
        user=user,
        password=password
    )
except psycopg2.Error as error:
    print(f"Error!!! {error}")

# conn.close()
# try:
#     conn = psycopg2.connect(
#         host=hostname,
#         dbname="Post_DB",
#         port=5432,
#         user="postgres",
#         password="postgres",
#     )
# except psycopg2.Error as error:
#     print(f"Error!!! {error}")

@app.get("/posts")
def post():
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM posts")
    
    posts = cur.fetchall()
    
    cur.close()

    return  {"data": posts}


@app.get("/posts/{id}")
def get_post(id: int):
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM posts WHERE id=%s", str(id))
    post = cur.fetchone()
    
    cur.close()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id '{id}' was not found")

    return post


@app.post("/posts/", status_code=status.HTTP_201_CREATED)
def post(post: Post):
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("INSERT INTO posts (title, content, id) VALUES (%s, %s, %s) RETURNING *", 
                    (post.title, post.message, post.id) )
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{error}")
    else:
        new_post = cur.fetchone()
    
    conn.commit()
    cur.close()
    
    return {"data": new_post} 


@app.put("/posts/{id}")
def update_post(id:int, post: Post):
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("UPDATE posts SET title=%s, content=%s WHERE id=%s RETURNING *", 
                    (post.title, post.message, str(id)) )

    updated_post = cur.fetchone()
    conn.commit()
    cur.close()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id '{id}' was not found")

    return updated_post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("DELETE FROM posts WHERE id=%s RETURNING *", (str(id)) )

    deleted_post = cur.fetchone()
    conn.commit()
    cur.close()

    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id '{id}' was not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

