import firebase_admin.auth
import firebase_admin
import dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import job_board
from .routers import job_search

dotenv.load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


default_app = firebase_admin.initialize_app()


app.include_router(job_search.router)

app.include_router(job_board.router)
