import dotenv
dotenv.load_dotenv()
import os
from fastapi import FastAPI
from app.routers import cover_letter, job_board
from .routers import job_search
from fastapi.middleware.cors import CORSMiddleware


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

app.include_router(cover_letter.router)
