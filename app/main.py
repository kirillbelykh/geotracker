from fastapi import FastAPI
from app.auth import quth_router

app = FastAPI()

app.include_router(quth_router)
