from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
import os 
from dotenv import load_dotenv

load_dotenv()
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')
SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)