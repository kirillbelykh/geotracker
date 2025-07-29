from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

    
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class UserLocation(BaseModel):
    latitude: float
    longitude: float
    timestamp: datetime
    
class UserConnect(BaseModel):
    jwt_token: str