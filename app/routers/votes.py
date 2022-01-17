from fastapi import FastAPI, status, Depends, APIRouter, HTTPException
from .. import models, schemas, oauth2, database
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)


'''
A vote means a row in votes table that links socialmediapost id with user id.
Presence of this row indicates the specified socialmediapost was liked/voted by the specified user

When rest api "vote" is sent, user specifies 2 things: 1. socialmediapost id 2. boolean
Boolean true means they want it liked/voted positively
Boolean false means they want it disliked/remove the positive vote previously done
'''
@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(vote: schemas.Vote, 
                db: Session = Depends(database.get_db), 
                current_user: str = Depends(oauth2.get_current_user)
                ):
    #check if that socialmediapost id is indeed valid
    post_query = db.query(models.SocialMediaPosts).filter(models.SocialMediaPosts.id == vote.social_media_post_id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post {vote.social_media_post_id} does not exist")
        
    vote_query = db.query(models.Votes).filter(models.Votes.social_media_post_id == vote.social_media_post_id,
        models.Votes.user_id == current_user.id)
    
    found_vote = vote_query.first()
    if vote.voted: # if boolean true - user wants this post to be liked or positively voted
        if found_vote: # socialmediapost id <==> user id ALREADY exists, meaning its already positively voted before
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
            detail=f"user {current_user.id} has already voted on social media postid {vote.social_media_post_id}")
        
        else: # if socialmediapost id <==> user id NOT FOUND, then add this vote
            new_vote = models.Votes(social_media_post_id = vote.social_media_post_id, user_id = current_user.id)
            db.add(new_vote)
            db.commit()
            return {"message": "successfully added vote"}
    
    
    else: # if boolean false - user wants this post to be disliked or remove positive vote previously done
        if found_vote: # socialmediapost id <==> user id exists, so we can dislike or remove positive vote
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"message": "successfully removed vote"}
        
        else: # if socialmediapost id <==> user id NOT FOUND, then there is nothing to dislike/remove vote
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"vote does not exist")
        
            

