from fastapi import FastAPI
from .database import Base, engine
from .routers import posts, users, auth


#  Create tables on startup if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

