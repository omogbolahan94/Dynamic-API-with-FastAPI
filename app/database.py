from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv(override=True)

hostname = os.getenv('HOST')
port = os.getenv('PORT')
db = os.getenv('DB_NAME')
user = os.getenv('USER')
password = os.getenv('PASSWORD')


DB_URL = f'postgresql://{user}:{password}@{hostname}:{port}/{db}'
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()