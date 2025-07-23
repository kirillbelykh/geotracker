from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String, Column, Integer

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
