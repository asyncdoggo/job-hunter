from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import UploadFile, File, Form, Depends
from fastapi import HTTPException
from fastapi import status
from fastapi import Request
from fastapi import Form
from ..job_utils.job_matching import JobMatcher
from ..job_utils.resume import ResumeParser
from ..job_utils.scraper import linkedinJobSpyScraper
from typing import List


router = APIRouter()

from pydantic import BaseModel

class JobMatcherRequest(BaseModel):
    search_term: str
    location: str


class JobMatcherResponse(BaseModel):
    matched_jobs: dict



parser = ResumeParser()
scraper = linkedinJobSpyScraper()
matcher = JobMatcher(scraper, parser)



from ..auth import get_current_user


@router.post("/job_matching")
async def job_matching(search_term: str=Form(...), location: str=Form(...), resume_file: List[UploadFile] = File(...), token: str = Depends(get_current_user)):
    with open("resume.pdf", "wb") as file_object:
        for chunk in resume_file:
            file_object.write(chunk.file.read())
    
    resume_file = "resume.pdf"

    matched_jobs = matcher.match_jobs(resume_file, search_term, location)

    matched_jobs = matched_jobs.to_json(orient="records")

    return JSONResponse(content={"matched_jobs": matched_jobs}, status_code=status.HTTP_200_OK)
    
    
