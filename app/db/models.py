from sqlalchemy import  Column, Integer, String, ForeignKey,VARCHAR,Date,Time,Boolean
from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String) 
    email = Column(String)
    password = Column(String)

    todos = relationship('Todo',back_populates='owner')


class Todo(Base):
    __tablename__ = 'todo'

    id= Column(Integer,primary_key=True)
    description = Column(String,index= True)
    day = Column(Date, nullable=True)
    time = Column(Time, nullable=True)
    complete = Column(Boolean,default=False)
    owner_id = Column(Integer,ForeignKey('users.id'))
    owner = relationship('User',back_populates='todos') 

     # New relationship
    files = relationship("File", back_populates="todo")


class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    file_path = Column(String, index=True)
    todo_id = Column(Integer, ForeignKey('todo.id'))

    # Relationship back to Todo
    todo = relationship("Todo", back_populates="files")