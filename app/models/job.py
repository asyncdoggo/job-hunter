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
    ONSITE = "onsite"
    HYBRID = "hybrid"
    REMOTE = "remote"
    NOT_SPECIFIED = "not specified"


class JobBoard(BaseModel):
    company_name: str
    position: str
    status: JobStatus
    salary: str
    job_type: JobType
    location: str
    job_url: str
    applied_date: str
    deadline: str
    id: Optional[str] = None
    user_id: Optional[str] = None