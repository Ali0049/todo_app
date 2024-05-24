from pydantic import BaseModel,ValidationError
from typing import Optional
from fastapi import FastAPI, File, UploadFile,Form
from datetime import date,time

class User(BaseModel):
    username : str
    email : str
    password : str


class User_show_change(BaseModel):
    email : str


class Todo(BaseModel):

    description: str
    day: Optional[date] 
    time: Optional[time] 
    complete : bool = False
    owner_id: Optional[int] = None

    class Config:
        from_attributes = True

class User_sho(BaseModel):
    username : str
    email : str
    todos : list[Todo]=[]

    class Config:
        from_attributes = True
    

class Todo_show(BaseModel):
    description : str
    day: Optional[date] = None
    time: Optional[time] = None
    complete : bool = False
    class Config:
        from_attributes = True  

class Login(BaseModel):
    email : str
    password : str

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    email : Optional[str] = None
    scopes: list[str] = []


