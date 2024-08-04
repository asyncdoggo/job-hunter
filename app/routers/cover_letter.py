import os
from app.auth import get_current_user
from app.job_utils.resume import ResumeParser
from ..job_utils.chatapi import GeminiAPI
from fastapi import APIRouter, Depends
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi import File
from fastapi import Form


gemini_key = os.getenv("GEMINI_API_KEY")

gemini_config = {
    "temperature": 0.5,
    "top_p": 1.0,
}

chatapi = GeminiAPI(api_key=gemini_key, generation_config=gemini_config)    

resume_parser = ResumeParser()

router = APIRouter()


prompt = """
Below is a resume and a job description both in plain text format. 
Understand the resume contents, especially experience, expertise, projects and skill set. 
Compare the resume and job description to understand the missing skills and requirements. 
Use your understanding to provide a curated cover letter, tailored for the provided job description. Make sure to add the job description keywords into the cover letter. Keep the cover letter short, crisp and professional.

Cover Letter format:
Single line introduction, very short
next paragraph: Why you are a good fit for the job, very short
next paragraph: How you can contribute to the company, very short
end with a closing line, very short

Note: DO NOT INCLUDE ANYTHING ELSE OTHER THAN COVER LETTER IN THE RESPONSE.

Resume:
{0}

Company Name: {1}
Job Title: {2}
Job Description:
{3}
"""

important_keys = ['name',"clean_data", "entities", 'emails', 'phones', 'experience', 'years', 'pos_frequencies', 'extracted_keywords', 'keyterms'] 


@router.post("/cover-letter")
async def cover_letter(job_description: str = Form(...), company_name: str = Form(...), job_title: str = Form(...), file: UploadFile = File(...),token: str = Depends(get_current_user)) -> dict:
    if "error" in token:
        raise HTTPException(status_code=400, detail=token["error"])

    resume = resume_parser.parse(file.file)

    if not resume:
        raise HTTPException(status_code=400, detail="Error processing resume")


    job_description = job_description.replace("\n", " ").replace("\t", " ").replace("\r", " ")
    company_name = company_name.replace("\n", " ").replace("\t", " ").replace("\r", " ")
    job_title = job_title.replace("\n", " ").replace("\t", " ").replace("\r", " ")
    
    prompt_text = prompt.format(resume["clean_data"], company_name, job_title, job_description)
    response = chatapi.get_response(prompt_text)

    return {"cover_letter": response}

    