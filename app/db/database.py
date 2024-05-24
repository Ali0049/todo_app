from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:ali0049@localhost:5432/Todo_App"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#by using this yeild pattern you ensure that database connections opend only when needed (when end point called)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()