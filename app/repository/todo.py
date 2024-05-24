# FastAPI app creation
from fastapi import FastAPI,status, HTTPException,Depends,File,UploadFile,Form
from sqlalchemy.orm import Session
#directory imports
from ..schema import schema
from ..db import models,database
from fastapi import UploadFile
from pathlib import Path
from ..config import oauth2
from typing import Optional
from datetime import date,time
from pydantic import BaseModel
import os

UPLOAD_DIRECTORY = "C:\\Users\\alij7\\Desktop\\todo_app\\app\\uploads"

def create_a_todo(description,day,time,complete,files,db,current_user):
    
    new_todo = models.Todo(
        description=description,
        day=day,
        time=time,
        complete=complete,
        owner_id=current_user.get('id')
    )

    # Add the todo to the database
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    # Handle file uploads if any
    filenames = []
    if files:
        for file in files:
            file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
            with open(file_path, "wb") as buffer:
                buffer.write(file.read())
            filenames.append(file.filename)

            # Create a new File instance
            new_file = models.File(
                filename=file.filename,
                file_path=file_path,
                todo_id=new_todo.id
            )
            db.add(new_file)

    db.commit()
    return {"new_todo": new_todo, "filenames": filenames}
    

def create_one_todo(response, db, current_user):
    # Create a new todo instance
    new_todo = models.Todo(
        description=response.description,
        day=response.day,
        time=response.time,
        owner_id=current_user.get('id')
    )
    # Add the todo to the database
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return new_todo

def get_everything(limit,db,current_user):
    todos = db.query(models.Todo).filter(models.Todo.owner_id==current_user.get('id')).all()
    if not todos:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                            detail='No todos ,add todos')
    return todos


def get_one_todo(id,db,current_user):
    todo=db.query(models.Todo).filter(models.Todo.owner_id==current_user.get('id') and models.Todo.id==id).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'no data found with id {id}')
    return todo

def get_with_date(Date,db,current_user):
    todo=db.query(models.Todo).filter(models.Todo.owner_id==current_user.get('id') and models.Todo.day==date).all()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'no data found with date {date}')
    return todo

def update_one_todo(id,response,db,current_user):
    todo = db.query(models.Todo).filter(models.Todo.owner_id==current_user.get('id') and models.Todo.id==id)
    if not todo.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'no data found with id {id}')
    todo.update({'description':response.description,
                 'day':response.day,
                 'time':response.time})
    db.commit()
    return {'details':'updated'}

def delete_one_todo(id,db,current_user):
    todo = db.query(models.Todo).filter(models.Todo.owner_id==current_user.get('id') and models.Todo.id==id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'no data found with id {id}')
    todo.delete(synchronize_session=False)
    db.commit()
    return {'details':'deleted'}

def get_similar_task(description,db,current_user):
    todo=db.query(models.Todo).filter(models.Todo.description==description).all()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'no task found with description: {description}')
    return todo