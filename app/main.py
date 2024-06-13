from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .routers import job_matching


app = FastAPI()

app.include_router(job_matching.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
