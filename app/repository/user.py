from fastapi import FastAPI,status, HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
#directory imports
from ..schema import schema
from ..repository import user
from ..config import hasihing
from ..db import models,database

def create_a_user(response,db):
    new_user = models.User(username=response.username,
                           email=response.email,
                           password=hasihing.Hash.get_password_hash(response.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_all_user(db:Session = Depends(database.get_db)):
    all_users = db.query(models.User).all()
    if not all_users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No User')
    return all_users

def get_one_user(id,db):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No User with id {id}')
    return user

def update_one_user(id,response,db):
    user = db.query(models.User).filter(models.User.id==id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No User with id {id}")
    user.update({'email': response.email})
    db.commit()
    return {'details':f'{response.email} : updated'}
