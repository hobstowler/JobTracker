from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

from server.controllers import JobController

app = FastAPI()


@app.get("/")
def root():
    return {"Hello": "World"}


@app.get("/item/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


class JobScrapeRequest(BaseModel):
    user_uuid: str
    source_name: str
    search_uuid: str


@app.post('/job/scrape')
async def scrape_for_jobs(job_scrape: JobScrapeRequest):
    job_controller = JobController()
    job_controller.scrape(job_scrape.user_uuid, job_scrape.source_name, job_scrape.search_uuid)

    return {
        'statusCode': 200
    }


class JobApplicationRequest(BaseModel):
    user_uuid: str
    job_uuids: list


@app.post('/job/apply')
async def apply_to_jobs(job_app: JobApplicationRequest):
    job_controller = JobController()

    job_controller.apply(user_uuid=job_app.user_uuid, job_uuids=job_app.job_uuids)

    return {"job_app": {
        "user": job_app.user_uuid,
        "job": job_app.job_uuids
    }}


@app.get('/job')
def get_jobs(uuid: str, q: Union[str, None] = None):
    job_controller = JobController()

    if q is None:
        jobs = job_controller.get_jobs(user_uuid=uuid)
    else:
        job_ids = q.split(',')
        jobs = job_controller.get_jobs(uuid, job_ids)

    return {
        'statusCode': 200,
        'content-type': 'application/json',
        'jobs': jobs
    }


@app.get('/company')
def get_companies(q: Union[str, None] = None):
    pass


@app.get('/company/{company_name}/jobs')
def get_company_jobs(company_name: str):
    pass
