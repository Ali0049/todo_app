# FastAPI app creation
from fastapi import FastAPI,status, HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
#directory imports
from ..db import models,database
from ..repository import user
from ..schema import schema



router = APIRouter(
    prefix='/User',
    tags=['User']

)

@router.post('/',status_code=status.HTTP_201_CREATED)
def create_user(response:schema.User,db:Session = Depends(database.get_db)):
    return user.create_a_user(response,db)

@router.get('/',status_code=status.HTTP_200_OK,)
def get_user(db:Session = Depends(database.get_db)):
    return user.get_all_user(db)

@router.get('/{id}',status_code=status.HTTP_200_OK,)
def get_a_user(id:int,db:Session =Depends(database.get_db)):
    return user.get_one_user(id,db)

@router.put('/',status_code=status.HTTP_202_ACCEPTED)
def update_user(id:int,response:schema.User_show_change,db:Session = Depends(database.get_db)):
    return user.update_one_user(id,response,db)