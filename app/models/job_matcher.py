from pydantic import BaseModel
from typing import List, Optional


class JobMatcher(BaseModel):
    search_term: str
    location: str
    distance: Optional[int] = 50
    job_type: Optional[str] = None
    proxies: Optional[List[str]] = None
    is_remote: Optional[bool] = False
    results_wanted: Optional[int] = 10
    easy_apply: Optional[bool] = False
    description_format: Optional[str] = "markdown"
    offset: Optional[int] = 0
    hours_old: Optional[int] = None
    verbose: Optional[int] = 2
    linkedin_fetch_description: Optional[bool] = False
    linkedin_company_ids: Optional[List[int]] = None

    class Config:
        schema_extra = {
            "example": {
                "search_term": "data scientist",
                "location": "New York",
                "distance": 50,
                "job_type": "fulltime",
                "proxies": ["user:pass@host:port", "localhost"],
                "is_remote": False,
                "results_wanted": 10,
                "easy_apply": False,
                "description_format": "markdown",
                "offset": 0,
                "hours_old": 24,
                "verbose": 2,
                "linkedin_fetch_description": False,
                "linkedin_company_ids": [1234, 5678]
            }
        }