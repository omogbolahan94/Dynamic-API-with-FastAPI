from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Optional, List
from sqlalchemy.orm import Session
from ..database import engine, get_db
from .. import models, schemas, utils, oauth2


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

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.PostResponse])
def post(db: Session = Depends(get_db)):
    # con = database_connector()
    # cur = con.cursor(cursor_factory=RealDictCursor)
    # cur.execute("SELECT * FROM posts")
    # posts = cur.fetchall()
    # cur.close()
    # con.close()

    posts = db.query(models.Post).all()
    return posts  


@router.get("/{id}",  response_model=schemas.PostResponse)
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


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def post(post: schemas.PostCreate, 
         db: Session = Depends(get_db), 
         current_user_id:int=Depends(oauth2.get_current_user)):
    
    new_post = models.Post(user_id=current_user_id, **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id:int, updated_post: schemas.PostUpdate, 
                db: Session = Depends(get_db),
                current_user_id:int=Depends(oauth2.get_current_user)):
    # cur = conn.cursor(cursor_factory=RealDictCursor)
    # cur.execute("UPDATE posts SET title=%s, content=%s WHERE id=%s RETURNING *", 
    #                 (post.title, post.message, str(id)) )
    # updated_post = cur.fetchone()
    # conn.commit()
    # cur.close()
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id '{id}' was not found")

    if post.user_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorize to perform this operation.")

    post.title = updated_post.title
    post.content = updated_post.content
    db.commit()
    db.refresh(post)

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, 
                db: Session = Depends(get_db),
                current_user_id:int=Depends(oauth2.get_current_user)):
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

    if post.user_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorize to perform this operation.")

    db.delete(post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

