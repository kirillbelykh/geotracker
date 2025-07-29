from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, datetime
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy import select
from .crud import get_db
from typing import Annotated
from .models import User

import os

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

oauth2scheme = OAuth2PasswordBearer(tokenUrl='auth/login')

async def create_jwt_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(db: Annotated[Session, Depends(get_db)], 
                           token: str = Depends(oauth2scheme)):
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get('sub')
        if email is None:
            return {"Email is none!"}
        user = db.query(User).filter(User.email==email).first()
        if user:
            return user
    except JWTError:
        raise HTTPException(status_code=401, detail='Unauthorized')
    