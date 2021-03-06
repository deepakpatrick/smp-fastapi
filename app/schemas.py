from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime


class UserCreateRequests(BaseModel):
    email: EmailStr
    password: str

#############
# Create a validation rule for the response generated by FastAPI
# The following will cause FastAPI error "response value is not valid dict". Add class Config below.
class UserCreateResponses(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config: # this is added to solve the above FastAPI error
        orm_mode = True
############  

class UserLogin(BaseModel):
    email: EmailStr
    password: str



# Create a validation rule for the social media posts generated by users
class BaseSocialMediaPostRequests(BaseModel): # "BaseUserRequests" is our own class name
    title : str
    contents : str
    published: bool = True
    
class SocialMediaPostCreate(BaseSocialMediaPostRequests):
    pass

class SocialMediaPostUpdate(BaseSocialMediaPostRequests):
    pass

##########################
# Create a validation rule for the response generated by FastAPI
# The following will cause FastAPI error "response value is not valid dict". Add class Config below.
class BaseSocialMediaPostResponses(BaseSocialMediaPostRequests): 
    id: int    
    created_at: datetime
    # owner_id: int
    owner: UserCreateResponses
    
    class Config: # this is added to solve the above FastAPI error
        orm_mode = True
##########################
class PostsWithOwnerVotesInfo(BaseModel):
    SocialMediaPosts: BaseSocialMediaPostResponses
    votes: int
    class Config: # this is added to solve the above FastAPI error
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    user_id: Optional[str] = None
    
class Vote(BaseModel):
    social_media_post_id: int
    voted: bool
