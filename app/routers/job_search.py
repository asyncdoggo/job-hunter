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
import json
import typing


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


@router.post("/job/match")
async def job_matching(search_term: str=Form(...), location: str=Form(...), resume_file: List[UploadFile] = File(...), token: str = Depends(get_current_user)):
    with open("resume.pdf", "wb") as file_object:
        for chunk in resume_file:
            file_object.write(chunk.file.read())
    
    resume_file = "resume.pdf"

    matched_jobs = matcher.match_jobs(resume_file, search_term, location)

    matched_jobs = matched_jobs.to_dict(orient="records")

    return JSONResponse(content={"matched_jobs": matched_jobs}, status_code=status.HTTP_200_OK)
    
    
@router.post("/job/search")
async def job_search(search_data: JobMatcherRequest, token: str = Depends(get_current_user)):
    try:
        jobs = scraper.get_jobs(search_data.search_term, search_data.location, results_wanted=10)

        jobs.fillna("", inplace=True)
        
        jobs = jobs.to_dict(orient="records")


        jobs = json.dumps(jobs, default=str)
        jobs = json.loads(jobs)

        return JSONResponse(content={"jobs": jobs}, status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))