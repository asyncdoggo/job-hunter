import json
from typing import List
from pydantic import BaseModel
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import UploadFile, File, Form, Depends
from fastapi import HTTPException
from fastapi import status
from ..auth import get_current_user
from ..job_utils.job_matching import JobMatcher
from ..job_utils.resume import ResumeParser
from ..job_utils.scraper import linkedinJobSpyScraper


router = APIRouter()


class JobSearchRequest(BaseModel):
    search_term: str
    location: str
    offset: int = 0


class JobMatcherResponse(BaseModel):
    matched_jobs: dict


parser = ResumeParser()
scraper = linkedinJobSpyScraper()
matcher = JobMatcher(scraper, parser)


@router.post("/job/match")
async def job_matching(search_term: str = Form(...), location: str = Form(...), resume_file: List[UploadFile] = File(...), token: str = Depends(get_current_user)):
    if "error" in token:
        raise HTTPException(status_code=400, detail=token["error"])

    with open("resume.pdf", "wb") as file_object:
        for chunk in resume_file:
            file_object.write(chunk.file.read())

    resume_file = "resume.pdf"

    matched_jobs = matcher.match_jobs(resume_file, search_term, location)

    matched_jobs = matched_jobs.to_dict(orient="records")

    return JSONResponse(content={"matched_jobs": matched_jobs}, status_code=status.HTTP_200_OK)


class JobResponseModel(BaseModel):
    id: str
    job_url: str
    title: str  # position
    company: str  # company_name
    location: str
    job_type: str


class JobSearchResponse(BaseModel):
    jobs: List[JobResponseModel]


@router.post("/job/search")
async def job_search(search_data: JobSearchRequest, token: str = Depends(get_current_user)):
    if "error" in token:
        raise HTTPException(status_code=400, detail=token["error"])

    try:
        jobs = scraper.get_jobs(
                                search_data.search_term,
                                search_data.location, 
                                results_wanted=10,
                                offset=search_data.offset * 10
                                )
        
        jobs.fillna("", inplace=True)

        jobs = jobs.to_dict(orient="records")

        jobs = json.dumps(jobs, default=str)
        jobs = json.loads(jobs)

        jobs = [{key: value for key, value in job.items(
        ) if key in JobResponseModel.model_fields} for job in jobs]

        return JSONResponse(content={"jobs": jobs}, status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
