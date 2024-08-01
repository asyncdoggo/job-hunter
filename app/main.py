import os
from fastapi import Depends, FastAPI
from app.routers import job_board
from .routers import job_search
from fastapi.middleware.cors import CORSMiddleware
import jwt
import datetime

import dotenv

dotenv.load_dotenv()

app = FastAPI()

allowed_origins = os.getenv("ALLOWED_ORIGINS").split(" ")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


import firebase_admin
import firebase_admin.auth


default_app = firebase_admin.initialize_app()


app.include_router(job_search.router)

app.include_router(job_board.router)
