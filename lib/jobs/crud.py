from fastapi import Request, HTTPException
from typing import Any
from uuid import uuid4

from ..interviews.functions import check_valid_company
from .models import CreateJob, UpdateJobStatus, DeleteJob

from ..database import db

async def create_job(req: Request, job: CreateJob):
    userId = req.state.user['userId']

    company = await check_valid_company(userId)

    job_dict = job.model_dump()

    job_dict['jobId'] = str(uuid4())
    job_dict['companyId'] = userId
    job_dict['companyName'] = company['companyName']
    job_dict['recruiterName'] = f"{company['firstName']} {company['lastName']}"

    await db["jobs"].insert_one(job_dict)

    return {'message': 'Job Created'}

async def update_status_job(req: Request, job: UpdateJobStatus):
    userId = req.state.user['userId']

    await check_valid_company(userId)

    count = await db['jobs'].count_documents({'userId': userId, 'jobId': job.jobId}, limit=1)
    if count <= 0:
        raise HTTPException(status_code=403, detail="Job not found")

    await db["jobs"].update_one(
        {'userId': userId, 'jobId': job.jobId},
        {"$set": {"status": job.status}}
    )

    return {'message': 'Job status updated'}

async def delete_job(req: Request, job: DeleteJob):
    userId = req.state.user['userId']

    await check_valid_company(userId)

    job_exists = await db['jobs'].find_one(
        {'userId': userId, 'jobId': job.jobId},
        {'jobName': 1}
    )
    if not job_exists:
        raise HTTPException(status_code=403, detail="Job not found")

    if job.messageConfirmation == f'Delete-{job_exists['jobName'].split()[0]}':
        await db['jobs'].delete_one({'userId': userId, 'jobId': job.jobId})
    else:
        raise HTTPException(status_code=403, detail="Invalid confirmation message")

    return {'message': 'Job Deleted'}

async def get_jobs_data(search: str | None, page: int = 1, size: int = 10):
    skip_records = (page - 1) * size

    query: dict[str, Any] = {'status': 'Active'}

    if search:
        query['jobName'] = {'$regex': search, '$options': 'i'}

    cursor = (
        db['jobs']
        .find(
            query,
            {'_id': 0}
        )
        .sort("createdAt", -1)
        .skip(skip_records)
        .limit(size)
    )

    return await cursor.to_list(length=size)