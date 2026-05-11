from fastapi import APIRouter, Request, Query

from lib.jobs.crud import create_job, update_status_job, delete_job, get_jobs_data, get_job_data_id
from lib.jobs.models import CreateJob, UpdateJobStatus, DeleteJob

job_router = APIRouter(prefix='/jobs')

@job_router.post('/create/', status_code=201)
async def create_job_route(req: Request, job: CreateJob):
    return await create_job(req, job)

@job_router.patch('/update/', status_code=201)
async def update_status_job_route(req: Request, job: UpdateJobStatus):
    return await update_status_job(req, job)

@job_router.delete('/delete/', status_code=201)
async def delete_job_route(req: Request, job: DeleteJob):
    return await delete_job(req, job)

@job_router.get('/data/')
async def jobs_data_route(
    search: str | None = Query(default=None, min_length=3),
    page: int = 1,
    size: int = Query(default=10, le=100)
):
    return await get_jobs_data(search, page, size)

@job_router.get("/data/{job_id}/")
async def job_data_id_route(job_id: str):
    return await get_job_data_id(job_id)