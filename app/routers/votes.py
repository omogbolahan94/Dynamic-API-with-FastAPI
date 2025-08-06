from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import database, schemas, oauth2, models


router = APIRouter(
    prefix="/votes",
    tags=["Votes"]
)


@router.post("/", status_code=status.HTTP_201_CREATED) 
def post(vote: schemas.VoteBase, 
         db: Session = Depends(database.get_db), 
         current_user_id:int=Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    vote_query = db.query(models.Votes).filter(
        models.Votes.post_id == vote.post_id,
        models.Votes.user_id == current_user_id
    )

    found_vote = vote_query.first()
    
    if vote.vote_direction == 1:
        # If vote already exists, raise conflict
        if found_vote:
            raise HTTPException(status_code=409, detail="User has already voted on this post")
        
        # Add vote
        new_vote = models.Votes(post_id=vote.post_id, user_id=current_user_id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote added successfully"}
    
    else:
        # If trying to delete a non-existent vote
        if not found_vote:
            raise HTTPException(status_code=404, detail="Vote does not exist")
        
        # Delete vote
        vote_query.delete()
        db.commit()
        return {"message": "Vote removed successfully"}