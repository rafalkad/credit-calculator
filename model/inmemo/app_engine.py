from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:admin123@localhost:5432/library"

Base = declarative_base()

app_engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=app_engine)
