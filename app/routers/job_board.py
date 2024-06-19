from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from app.auth import get_current_user
from app.models.job import JobBoard
from app.db.firebasedb import FireBaseDatabase




router = APIRouter()


def get_db():
    db = FireBaseDatabase()
    try:
        yield db
    finally:
        db.close()

# Job Board query
@router.get("/job/board")
async def job_board_get(token: str = Depends(get_current_user), db: FireBaseDatabase = Depends(get_db)) -> dict:
    if "error" in token:
        raise HTTPException(status_code=400, detail=token["error"])
    
    user_id = token["user_id"]
    try:
        jobs = db.query({"user_id": user_id})
        return {"jobs": jobs}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Job Board insert
@router.post("/job/board")
async def job_board_insert(job: JobBoard, token: str = Depends(get_current_user), db: FireBaseDatabase = Depends(get_db)) -> dict:
    if "error" in token:
        raise HTTPException(status_code=400, detail=token["error"])

    job_data = job.model_dump()
    job_data["user_id"] = token["user_id"]
    try:
        db.insert(job_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Job added successfully", "job": job_data}

# Job Board update
@router.put("/job/board")
async def job_board_update(job: JobBoard, token: str = Depends(get_current_user), db: FireBaseDatabase = Depends(get_db)) -> dict:
    if "error" in token:
        raise HTTPException(status_code=400, detail=token["error"])

    job_data = job.model_dump()
    job_data["user_id"] = token["user_id"]
    try:
        db.update(job_data)
        return {"message": "Job updated successfully", "job": job_data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Job Board delete
@router.delete("/job/board/{job_id}")
async def job_board_delete(job_id: str, token: str = Depends(get_current_user), db: FireBaseDatabase = Depends(get_db)) -> dict:
    if "error" in token:
        raise HTTPException(status_code=400, detail=token["error"])

    user_id = token["user_id"]
    try:
        db.delete({"user_id": user_id, "id": job_id})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Job deleted successfully"}