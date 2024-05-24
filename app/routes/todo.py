# FastAPI app creation
from fastapi import FastAPI,status, HTTPException,Depends,APIRouter,File,UploadFile,Form
from sqlalchemy.orm import Session
#directory imports
from ..db import models,database
from ..schema import schema
from ..repository import user,todo
from .import user
from ..config import oauth2
from secrets import token_hex
from typing import Union
from typing import Annotated,Optional
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os
from datetime import date,time


router = APIRouter(
    prefix='/todo',
    tags=['TODOs'],
)


class TodoCreate(BaseModel):
    description: str
    day: Optional[date] = None
    time: Optional[time] = None
    complete : bool = False


@router.post('/file',status_code=status.HTTP_201_CREATED)
def create_todo(
    description: str = Form(...),
    day: Optional[date] = Form(...),
    time: Optional[time] = Form(...),
    complete: bool = Form(False),
    files: Optional[list[UploadFile]] = File(None),
    db: Session = Depends(database.get_db),
    current_user: schema.User = Depends(oauth2.get_current_user)
):
    todo_data = schema.Todo(
        description=description,
        day=day,
        time=time,
        complete=complete
    )
    return todo.create_a_todo(todo_data.description, todo_data.day, todo_data.time, todo_data.complete, files, db, current_user)

@router.get('/',status_code=status.HTTP_200_OK)
def get_all_todos(limit:int=5,db:Session=Depends(database.get_db),current_user:schema.User = Depends(oauth2.get_current_user)):
    return todo.get_everything(limit,db,current_user)

@router.get('/{id}',status_code=status.HTTP_200_OK)
def get_a_todo(id:int,db:Session=Depends(database.get_db),current_user:schema.User = Depends(oauth2.get_current_user)):
    return todo.get_one_todo(id,db,current_user)

@router.get('/{Date}',status_code=status.HTTP_200_OK)
def get_with_date(Date:date,db:Session=Depends(database.get_db),current_user:schema.User = Depends(oauth2.get_current_user)):
    return todo.get_witfah_date(Date,db,current_user)

@router.get('/{description}',status_code=status.HTTP_200_OK)
def get_similar(desciption:str,db:Session=Depends(database.get_db),current_user:schema.User = Depends(oauth2.get_current_user)):
    return todo.get_similar_task(desciption,db,current_user)

@router.put('/{id}',status_code=status.HTTP_200_OK)
def update_a_todo(id:int,response:schema.Todo,db:Session=Depends(database.get_db),current_user:schema.User = Depends(oauth2.get_current_user)):
    return todo.get_one_todo(id,db,current_user)

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_a_todo(id:int,db:Session = Depends(database.get_db),current_user:schema.User = Depends(oauth2.get_current_user)):
    return todo.delete_one_todo(id,db,current_user)

