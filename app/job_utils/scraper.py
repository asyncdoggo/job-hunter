import abc
from jobspy import scrape_jobs



class Scraper(abc.ABC):
    def __init__(self):
        pass

    def get_jobs(self, search_term):
        pass


class JobSpyScraper(Scraper):
    """
    Optional
├── site_name (list|str): 
|    linkedin, zip_recruiter, indeed, glassdoor 
|    (default is all four)
│
├── search_term (str)
│
├── location (str)
│
├── distance (int): 
|    in miles, default 50
│
├── job_type (str): 
|    fulltime, parttime, internship, contract
│
├── proxies (list): 
|    in format ['user:pass@host:port', 'localhost']
|    each job board will round robin through the proxies
│
├── is_remote (bool)
│
├── results_wanted (int): 
|    number of job results to retrieve for each site specified in 'site_name'
│
├── easy_apply (bool): 
|    filters for jobs that are hosted on the job board site
│
├── description_format (str): 
|    markdown, html (Format type of the job descriptions. Default is markdown.)
│
├── offset (int): 
|    starts the search from an offset (e.g. 25 will start the search from the 25th result)
│
├── hours_old (int): 
|    filters jobs by the number of hours since the job was posted 
|    (ZipRecruiter and Glassdoor round up to next day.)
│
├── verbose (int) {0, 1, 2}: 
|    Controls the verbosity of the runtime printouts 
|    (0 prints only errors, 1 is errors+warnings, 2 is all logs. Default is 2.)

├── linkedin_fetch_description (bool): 
|    fetches full description and direct job url for LinkedIn (Increases requests by O(n))
│
├── linkedin_company_ids (list[int]): 
|    searches for linkedin jobs with specific company ids
|
├── country_indeed (str): 
|    filters the country on Indeed & Glassdoor (see below for correct spelling)
├── Indeed limitations:
|    Only one from this list can be used in a search:
|    - hours_old
|    - job_type & is_remote
|    - easy_apply
│
└── LinkedIn limitations:
|    Only one from this list can be used in a search:
|    - hours_old
|    - easy_apply

    """

    def __init__(self):
        super().__init__()

    def get_jobs(self, site_names: list = [], search_term: str="", location: str = "", distance: int = 50, job_type: str = None, proxies: list = None, is_remote: bool = False, results_wanted: int = 10, easy_apply: bool = False, description_format: str = "markdown", offset: int = 0, hours_old: int = 0, verbose: int = 2, linkedin_fetch_description: bool = False, linkedin_company_ids: list = None, country_indeed: str = 'usa'):
        jobs = scrape_jobs(
            site_name=site_names,
            search_term=search_term,
            location=location,
            distance=distance,
            job_type=job_type,
            proxies=proxies,
            is_remote=is_remote,
            results_wanted=results_wanted,
            easy_apply=easy_apply,
            description_format=description_format,
            offset=offset,
            hours_old=hours_old,
            verbose=verbose,
            linkedin_fetch_description=linkedin_fetch_description,
            linkedin_company_ids=linkedin_company_ids,
            country_indeed=country_indeed
        )

        return jobs
    

import bs4
import requests

class linkedinJobSpyScraper(JobSpyScraper):
    def __init__(self):
        super().__init__()

    def get_jobs(self, search_term: str, location: str = "", distance: int = 50, job_type: str = "", proxies: list = None, is_remote: bool = False, results_wanted: int = 10, easy_apply: bool = False, description_format: str = "markdown", offset: int = 0, hours_old: int = 0, verbose: int = 2, linkedin_company_ids: list = None, country_indeed: str = "usa"):
        jobs = super().get_jobs(site_names=["linkedin"], search_term=search_term, location=location, distance=distance, job_type=job_type, proxies=proxies, is_remote=is_remote, results_wanted=results_wanted, easy_apply=easy_apply, description_format=description_format, offset=offset, hours_old=hours_old, verbose=verbose, linkedin_company_ids=linkedin_company_ids, country_indeed=country_indeed)
        # Check if jobs is not empty dataframe
        if jobs.empty:
            return jobs 
        # jobs["description"] = jobs["job_url"].apply(self._scrape_data_from_linkedin)
        return jobs
    
    def _scrape_data_from_linkedin(self, url: str):
        """
        Deprecated
        """
        return DeprecationWarning("This method is deprecated. Cannot access LinkedIn job pages using requests anymore.")

        finding_id = "job-details"
        content = requests.get(url).content
        soup = bs4.BeautifulSoup(content, "html.parser")
        description = soup.find("div", {"id": finding_id})
        try:
            # get all paragraphs in the description
            paragraphs = description.find_all("p")
            # join all paragraphs together
            description = "\n".join([p.text for p in paragraphs])
        except:
            description = ""
        return description 
