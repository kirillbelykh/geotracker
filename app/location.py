from fastapi import APIRouter, HTTPException, Depends, status, Query
from .models import Location, User
from .utils import get_current_user
from .schemas import UserLocation
from sqlalchemy.orm import Session
from sqlalchemy import insert
from .crud import get_db
from typing import Annotated
from datetime import datetime, timedelta
location_router = APIRouter(prefix='/location', tags=['location'])

@location_router.post('/', status_code=201)
async def save_location(
    location_data: UserLocation,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)] 
):
    try:
        new_location = Location(
            user_id=current_user.id,
            latitude=location_data.latitude,
            longitude=location_data.longitude,
            timestamp=location_data.timestamp
        )
        db.add(new_location)
        db.commit()
        
        return {"message": "Location saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@location_router.get('/track/{user_id}', status_code=200)
async def get_user_location(
    user_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    date: str = Query(..., description="Date in YYYY-MM-DD format")):
    """Возвращает все координаты за указанную дату"""
    
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail='Access denied')
    
    try:
        start_date = datetime.strptime(date, "%Y-%m-%d")
        end_date = start_date + timedelta(days=1)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")
    
    result = db.query(Location).filter(
        Location.user_id == user_id,
        Location.timestamp >= start_date,
        Location.timestamp < end_date
    ).order_by(Location.timestamp).all()
    
    return [
        {
            'latitude': loc.latitude,
            'longitude': loc.longitude,
            'timestamp': loc.timestamp
        } for loc in result
    ]
    
@location_router.get('/history', status_code=200)
async def get_location_history(
                               db: Annotated[Session, Depends(get_db)], 
                               current_user: Annotated[User, Depends(get_current_user)],
                               limit: int = Query(100, ge=1, le=500),
                               offset: int = Query(0, ge=0),
                               start_date: str = Query(..., description="Start period of date in YYYY-MM-DD format"),
                               end_date: str = Query(..., description="End period of date in YYYY-MM-DD format")):
    
    try:
        if datetime.strptime(start_date, "%Y-%m-%d"):
            if datetime.strptime(end_date, "%Y-%m-%d"):
                result = db.query(Location).filter(Location.user_id==current_user.id,
                                       Location.timestamp>=start_date,
                                       Location.timestamp<=end_date).order_by(Location.timestamp).limit(limit).offset(offset)
                return [
        {
            'latitude': loc.latitude,
            'longitude': loc.longitude,
            'timestamp': loc.timestamp
        } for loc in result
    ]
                
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")
    
    
    
    
@location_router.get('/latest', status_code=200)
async def get_latest_location(db: Annotated[Session, Depends(get_db)], 
                            current_user: Annotated[User, Depends(get_current_user)]):
    
    latest_location = db.query(Location).filter(Location.user_id==current_user.id,
                                                Location.timestamp<=datetime.now()).first()
    
    return [
        {
            'latitude': latest_location.latitude,
            'longitude': latest_location.longitude,
            'timestamp': latest_location.timestamp
        } 
    ]
    
    