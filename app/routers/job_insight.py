from ..job_utils.chatapi import GeminiAPI
from fastapi import APIRouter


gemini_key = "GEMINI_API_KEY"

gemini_config = {
    "temperature": 0.5,
    "top_p": 1.0,
}

chatapi = GeminiAPI(api_key=gemini_key, generation_config=gemini_config)


router = APIRouter()


prompt = """
Below is a resume and a job description both in plain text format. 
Understand the resume contents, especially experience, expertise, projects and skill set. 
Compare the resume and job description to understand the missing skills and requirements. 
Use your understanding to provide a curated cover letter, tailored for the provided job description. Make sure to add the job description keywords into the cover letter. Keep the cover letter short, crisp and professional. Do not exceed 3 paragraphs. 
Note: DO NOT INCLUDE ANYTHING ELSE OTHER THAN COVER LETTER IN THE RESPONSE.
"""


# @router.post("/job-insight")
# def job_insight(resume_file: UploadFile = File(...), job_description: str = Form(...), token: str = Depends(get_current_user)) -> dict:
#     pass
