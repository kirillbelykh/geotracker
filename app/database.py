from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

engine = create_engine('postgresql+psycopg2://newest_user:qwerty@localhost/geo_db')
SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)