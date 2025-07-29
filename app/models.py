from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import String, Column, Integer, ForeignKey, Float, DateTime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    

class Location(Base):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    latitude = Column(Float)
    longitude = Column(Float)
    timestamp = Column(DateTime)