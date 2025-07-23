from fastapi import Depends, status, HTTPException
from fastapi.routing import APIRouter
from schemas import UserCreate
from passlib.context import CryptContext
from models import User
from crud import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import insert, select

quth_router = APIRouter(prefix='/register', tags=['register'])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)
    

@quth_router.post('/')
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
    