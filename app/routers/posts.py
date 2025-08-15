from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import engine, get_db
from .. import models, schemas, utils, oauth2

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.PostWithVotes])
def post(db: Session = Depends(get_db), current_user_id:int=Depends(oauth2.get_current_user),
        limit:int=10, skip:int=0, search: Optional[str]=""): # limit, search and skip path parameter

    all_posts = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(
                     models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(
                     models.Post.id).filter(
                     models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return [{"post": post, "votes": votes} for post, votes in all_posts]


@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
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

