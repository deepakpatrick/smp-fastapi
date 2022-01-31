# Get FastAPI related
from fastapi import FastAPI, status, Depends, APIRouter, HTTPException


# Get SQLAlchemy related
from sqlalchemy.orm import Session
from sqlalchemy import func

# Get other Python packages
from typing import List, Optional



# Get python files/folders(packages) we created
from .. import models, schemas, oauth2, database



router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

'''
Rest api GET all - gets all social media posts from the social_media_table
'''
@router.get("/",response_model=List[schemas.PostsWithOwnerVotesInfo])
async def get_posts(db: Session = Depends(database.get_db),
                    # current_user: str = Depends(oauth2.get_current_user),
                    limit: int = 10, # will fetch a max of 10 results only
                    skip: int = 0,
                    search: Optional[str] = ""
                    ):
    # posts = db.query(models.SocialMediaPosts).filter(
    #     models.SocialMediaPosts.title.contains(search)).limit(limit_count).offset(skip_count).all()
    '''
    # if you want posts of logged in current user only then do this:
    posts = db.query(models.SocialMediaPosts).filter(models.SocialMediaPosts.owner_id == current_user.id).all()
    '''
    posts = db.query(models.SocialMediaPosts, func.count(models.Votes.social_media_post_id).label("votes")).join(
                models.Votes, 
                models.Votes.social_media_post_id == models.SocialMediaPosts.id,
                isouter=True).group_by(models.SocialMediaPosts.id).filter(models.SocialMediaPosts.title.contains(search)).limit(limit).offset(skip).all()
    print(posts)                                       
    return posts

'''
Rest api POST - creates one social media post and inserts into social_media_table
'''
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.BaseSocialMediaPostResponses)
async def create_posts(smp_create: schemas.SocialMediaPostCreate, 
                       db: Session = Depends(database.get_db),
                       current_user: str = Depends(oauth2.get_current_user)
                       ):
    
    
    print(smp_create)
    # assign social_media_posts table column name values with values received from body of post request
    # new_post = models.SocialMediaPosts(title = smp_create.title,
    #                        contents = smp_create.contents,
    #                        published = smp_create.published)
    
    ######### or use the python dictionary unpacking ##########
    new_post = models.SocialMediaPosts(owner_id = current_user.id, **smp_create.dict()) # this eliminates remembering individual json fields/column names
    print(new_post)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

'''
Rest api GET - get one specific social media post based on its ID
'''
@router.get("/{id}", response_model=schemas.PostsWithOwnerVotesInfo)
async def get_post(id: int, 
                   db: Session = Depends(database.get_db),
                   current_user: str = Depends(oauth2.get_current_user)
                   ):
    # post_query1 = db.query(models.SocialMediaPosts).filter(models.SocialMediaPosts.id == id)
    # post1 = post_query1.first() 
    # if post1.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    #                         detail=f"Not authorized to perform this operation")
    # .first() gets the first match. without this trying to locate goes in recursive unending loop
    post_query2 = db.query(models.SocialMediaPosts, func.count(models.Votes.social_media_post_id).label("votes")).join(
                models.Votes, 
                models.Votes.social_media_post_id == models.SocialMediaPosts.id,
                isouter=True).group_by(models.SocialMediaPosts.id).filter(models.SocialMediaPosts.id == id)
    
    post2 = post_query2.first() 
    if post2 is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"postid {id} not found")
    
    return post2

'''
Rest api DELETE - delete one specific social media post based on its ID
'''
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, 
                      db: Session = Depends(database.get_db),
                      current_user: str = Depends(oauth2.get_current_user)
                      ):
    post_query = db.query(models.SocialMediaPosts).filter(models.SocialMediaPosts.id == id)  # try to locate the id  
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"postid {id} not found")    
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden to perform this operation")
        
    post_query.delete(synchronize_session=False) # if id found then delete it    
    db.commit()    
    return f"postid {id} deleted successfully"

'''
Rest api PUT - modifies one specific social media post based on its ID
'''    
@router.put("/{id}", response_model=schemas.BaseSocialMediaPostResponses)
async def update_post(id: int, 
                      smp_update: schemas.SocialMediaPostUpdate, 
                      db: Session = Depends(database.get_db),
                      current_user : str = Depends(oauth2.get_current_user)
                      ):
    post_query = db.query(models.SocialMediaPosts).filter(models.SocialMediaPosts.id == id)  # try to locate the id
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"postid {id} not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden to perform this operation")
    
    post_query.update(smp_update.dict(), synchronize_session=False)
    db.commit()
    return post   