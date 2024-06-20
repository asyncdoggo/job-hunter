
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

class JobType(str, Enum):
    Onsite = "onsite"
    Hybrid = "hybrid"
    REMOTE = "remote"


class JobBoard(BaseModel):
    company_name: str
    position: str
    status: JobStatus
    salary: str
    job_type: str
    location: str
    job_url: str
    applied_date: str
    deadline: str
    description: str
    id: str  = None
    user_id: Optional[str] = None