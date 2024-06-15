
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class JobStatus(str, Enum):
    WISHLIST = "wishlist"
    APPLIED = "applied"
    INTERVIEW = "interview"
    OFFER = "offer"
    GHOSTED = "ghosted"
    REJECTED = "rejected"
    FOLLOW_UP = "follow up"


class JobBoard(BaseModel):
    status: JobStatus
    company_name: str
    position: str
    salary: str
    location: str
    job_url: str
    user_id: Optional[str] = None
    job_id: Optional[str]  = None