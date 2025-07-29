from fastapi import Depends, status, HTTPException
from fastapi.routing import APIRouter
from .schemas import UserCreate, UserLogin, UserConnect
from passlib.context import CryptContext
from .models import User
from .crud import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import insert, select
from .utils import create_jwt_token, get_current_user
import os 
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

auth_router = APIRouter(prefix='/auth', tags=['auth'])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)
    

@auth_router.post('/register', status_code=201)
async def register(user_info: UserCreate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(User).where(User.email==user_info.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    elif not existing_user:
        db.execute(insert(User).values(email=user_info.email, hashed_password=hash_password(user_info.password)))
        db.commit()
        return {
            'status_code': status.HTTP_201_CREATED,
            'message': 'User Created'
        }
        
@auth_router.post('/login', status_code=200)
async def login(user_info: UserLogin, db: Annotated[Session, Depends(get_db)]):
    existing_user = db.scalar(select(User).where(User.email==user_info.email))
    if existing_user:
        password_check = pwd_context.verify(user_info.password, existing_user.hashed_password)
        if password_check:
            payload = {
                'sub': str(existing_user.email)
            }
            token = await create_jwt_token(payload, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
            return {
                'status_code': status.HTTP_200_OK,
                'jwt_token': token,
                'token_type': 'Bearer',
                'message': 'Login successful'
            }
        else:
            raise HTTPException(status_code=401, detail="Incorrect password")
        
@auth_router.get('/me')
async def get_me(connection_data: UserConnect, current_user: User = Depends(get_current_user)):
    return {'email': current_user.email}


    