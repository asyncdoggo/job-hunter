import pandas as pd


class JobMatcher:
    def __init__(self, scraper, parser) -> None:
        self.scraper = scraper
        self.parser = parser

    def match_jobs(self, resume_file: str, search_term: str, location: str = ""):
        # parse resume
        resume_data = self.parser.parse(resume_file)
        # get jobs
        jobs = self.scraper.get_jobs(
            search_term=search_term, location=location)
        # match jobs
        matched_jobs = self._match_jobs(resume_data, jobs)
        return matched_jobs

    def _match_jobs(self, resume_data, jobs):
        matched_jobs = []
        for idx, job in jobs.iterrows():
            job_keywords = set(job["description"].split())
            resume_keywords = set(resume_data["extracted_keywords"])
            common_keywords = job_keywords.intersection(resume_keywords)
            if len(common_keywords) > 0:
                matched_jobs.append(job)

        matched_jobs = pd.concat(matched_jobs, axis=1).T
        matched_jobs.columns = jobs.columns

        return matched_jobs
