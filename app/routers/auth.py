# Get FastAPI related
from fastapi import FastAPI, status, Depends, APIRouter, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

# Get SQLAlchemy related
from sqlalchemy.orm import Session

# Get other Python packages
from typing import List

# Get python files/folders(packages) we created
# from current location get the following files
from .. import database, models, schemas, utils, oauth2


router = APIRouter(
    tags=["Authentication"]
    )

@router.post('/login', response_model=schemas.Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), 
                db: Session = Depends(database.get_db)
                ):
    
    '''
    OAuth2PasswordRequestForm will return only "username" and "password" in this format:
    {
        "username":"asdasd"
        "password":"dfsdfsd"
    }
    It does not differentiate between username and email
    
    So user_credentials "username" will have the email id
    '''
    
    
    
    # locate the email id of the user trying to login
    user_record = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()
    if not user_record: # is None:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, 
                            detail = f"Invalid credentials")
    
    '''
    If email id found, compare password supplied by user during login (hash it first), with
    hashed password stored in "users" table for that user
    '''
    result = utils.verify_password(user_credentials.password, user_record.password) 
    if not result:
        raise HTTPException(status.HTTP_403_FORBIDDEN, 
                            detail="Invalid Credentials")
    
    # create a token
    access_token = oauth2.create_access_token( token_pay_load = {"user_id":user_record.id} )
    # return token
    return {"access_token" : access_token, "token_type": "bearer"}
    