from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, oauth2
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from . import database, models
from . config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# 3 things required
# SECRET_KEY
# Algo
# Expiration time for tokens

'''
Payload = Can be null or any relevant info e.g. user_id. Can also be a combo. e.g. userId + token_expiry_time
Secret_key = A specific 256 bit alphanumeric text available and stored only in API server
Algo_type (Header) = Algo (e.g. HS256)  ---> Type (e.g. JWT). Together this will be a constant

           
Token = Algo_type Header + Payload + Signature
where Signature = HS256 hashing of the following 3 items:
                    {
                        1. Payload (Base64URL encoded)
                        2. Secret Key (256 bits)
                        3. Algo_type Header (Base64URL encoded)                
                    }
'''


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes 

def create_access_token(token_pay_load: dict):
    
    pay_load = token_pay_load.copy()    
    # calculating token_expiry_time from current time and adding that info to Payload
    expires = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    print(datetime.now())
    print(expires)
    expires = expires.timestamp()     # converts datetime object "2022-01-10 02:03:24.245260" to string(seconds) "1641805404.24526"
    
    pay_load.update({"expires": expires}) # now payload has "user_id" and "token_expiry_time"
    
    #create access token
    print(pay_load)
    access_token = jwt.encode(claims=pay_load, 
                              key=SECRET_KEY, 
                              algorithm=ALGORITHM)
    return access_token
    
def get_current_user(access_token: str = Depends(oauth2_scheme),
                     db: Session = Depends(database.get_db)
                     ):  
    
    
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail=f"Could not validate credentials",
                                          headers={"WWW-Authenticate":"Bearer"}
                                          )    
    try:
        decoded_token = jwt.decode(token=access_token, 
                             key=SECRET_KEY, 
                             algorithms=[ALGORITHM]) # there could be more than 1 algo, hence a list
        # print(decoded_token)       
    except JWTError:
        raise credentials_exception
    

    user_id: str = decoded_token.get("user_id")
    if user_id is None:
        raise credentials_exception
    
    
    expires = decoded_token.get("expires")
    if expires is None:
        raise credentials_exception       
    if datetime.now() > datetime.fromtimestamp(expires) :
        raise credentials_exception    
    current_user = db.query(models.Users).filter(models.Users.id == user_id).first()    
    return current_user 

    
 