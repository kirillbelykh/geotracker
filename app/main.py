from fastapi import FastAPI
from .auth import auth_router
from .location import location_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(location_router)
