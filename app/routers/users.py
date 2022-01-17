# Get FastAPI related
from fastapi import FastAPI, status, Depends, APIRouter, HTTPException


# Get SQLAlchemy related
from sqlalchemy.orm import Session

# Get other Python packages
from typing import List

# Get python files/folders(packages) we created
from .. import models, schemas, utils
from ..database import get_db # from our database.py file get "get_db" function


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

'''
Rest api POST - creates one user into users table
'''
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreateResponses )
async def create_users(user: schemas.UserCreateRequests,  
                       db: Session = Depends(get_db)                       
                       ):
    
    # hash the password - user.password
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    # new_user = models.Users(email = user.email,
    #                        password = user.password,
    #                        )
    
    ####### or unpack the dictionary
    new_user = models.Users(**user.dict())
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

'''
Rest api GET - get one specific user's details based on their ID
'''
@router.get("/{id}", response_model=schemas.UserCreateResponses)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id) 
    # .first() gets the first match. without this trying to locate goes in recursive unending loop
    if user.first() is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"user id {id} not found")
    return user.first()