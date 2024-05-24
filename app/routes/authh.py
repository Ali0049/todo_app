from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..schema import schema
from ..db import database ,models
from ..config import hasihing
from sqlalchemy.orm import Session
from datetime import datetime, timedelta,timezone
from ..config import token
from fastapi import APIRouter

router = APIRouter(
    prefix = '/login_JWT',
    tags = ['Authentication']
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
ACCESS_TOKEN_EXPIRE_MINUTES = 30




@router.post('/')
def validate_password(response : OAuth2PasswordRequestForm = Depends() , db :Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email==response.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='user not found with this email')
    
    if not hasihing.Hash.verify_password(response.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='invalid password')

    token_expires = timedelta(minutes=
                              ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token.create_access_token(user.email,user.id,expires_delta=token_expires)
    
    return schema.Token(access_token=access_token, token_type="bearer")
    


