
from fastapi import  FastAPI
from . import models
from dotenv import load_dotenv

from .database import engine
from .router import posts, users,auth,vote
from fastapi.middleware.cors import CORSMiddleware
#models.Base.metadata.create_all(bind=engine)
app = FastAPI()
import os

load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message":"Hello World"}
