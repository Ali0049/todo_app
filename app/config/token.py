
from ..schema import schema
from datetime import datetime, timedelta,timezone
from typing import Union
from jose import JWTError, jwt


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



def create_access_token(email:str, user_id:int , expires_delta: Union[timedelta, None] = None):
    to_encode = {'sub':email,'id':user_id}
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_id : int =payload.get('id')
        if email is None:
            raise credentials_exception
        token_data = schema.TokenData(email=email)
        return {"id": user_id, "email": email}
    except JWTError:
        raise credentials_exception

