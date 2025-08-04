from fastapi import FastAPI, Response, status, HTTPException, Depends
from psycopg2.extras import RealDictCursor
from pathlib import Path 
from . import models, schemas, utils
from .database import Base, engine
from .routers import posts, users, auth


#  Create tables on startup if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

