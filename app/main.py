from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
import psycopg2
import asyncpg
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from pathlib import Path 
from . import models, schemas
from sqlalchemy.orm import Session
from .database import Base, engine, get_db



load_dotenv(override=True)

#  Create tables on startup if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()


# db = models.SessionLocal()
# new_post = Post(title="First Post", message="Hello, FastAPI with SQLAlchemy!")
# db.add(new_post)
# db.commit()
# db.refresh(new_post)

class Post(BaseModel):
    title: str
    message: str
    id: int
    # rating: Optional[int] = None

# hostname = os.getenv('HOST')
# port = os.getenv('PORT')
# db = os.getenv('DB_NAME')
# user = os.getenv('USER')
# password = os.getenv('PASSWORD')


# psycopg connection
# def database_connector():
#     try:
#         conn = psycopg2.connect(
#             host=hostname,
#             port=port,
#             dbname=db,
#             user=user,
#             password=password
#         )
#         print("connection successful") 
#     except psycopg2.Error as error:
#         # if conn: conn.rollback()
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Something is wrong: '{error}'")

#     else:
#         return conn


@app.get("/posts", response_model=List[schemas.PostResponse])
def post(db: Session = Depends(get_db)):
    # con = database_connector()
    # cur = con.cursor(cursor_factory=RealDictCursor)
    # cur.execute("SELECT * FROM posts")
    # posts = cur.fetchall()
    # cur.close()
    # con.close()

    posts = db.query(models.Post).all()
    return posts  


@app.get("/posts/{id}",  response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    # con = database_connector()
    # cur = con.cursor(cursor_factory=RealDictCursor)
    # cur.execute("SELECT * FROM posts WHERE id=%s", str(id))
    # post = cur.fetchone()
    # cur.close()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id '{id}' was not found")

    return post


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    
    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@app.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id:int, updated_post: schemas.PostUpdate, db: Session = Depends(get_db)):
    # cur = conn.cursor(cursor_factory=RealDictCursor)
    # cur.execute("UPDATE posts SET title=%s, content=%s WHERE id=%s RETURNING *", 
    #                 (post.title, post.message, str(id)) )
    # updated_post = cur.fetchone()
    # conn.commit()
    # cur.close()
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id '{id}' was not found")

    post.title = updated_post.title
    post.content = updated_post.content
    db.commit()
    db.refresh(post)

    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db)):
    # con = database_connector()
    # cur = con.cursor(cursor_factory=RealDictCursor)
    # cur.execute("DELETE FROM posts WHERE id=%s RETURNING *", (str(id)) )
    # deleted_post = cur.fetchone()
    # con.commit()
    # cur.close()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id '{id}' was not found")

    db.delete(post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

