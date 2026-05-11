from fastapi import Request, HTTPException
from uuid import uuid4
from datetime import datetime
from zoneinfo import ZoneInfo

from .models import CreateApplication, UpdateApplication
from ..interviews.functions import check_valid_company

from ..database import db

async def create_application(req: Request, application: CreateApplication):
    userId = req.state.user['userId']

    application_exists = await db['applications'].count_documents(
        {'jobId': application.jobId, 'candidateId': userId},
        limit=1
    )

    if application_exists > 0:
        raise HTTPException(status_code=403, detail='You have already applied for this job')
    
    candidate_data = await db['users'].find_one(
        {'userId': userId},
        {'_id': 0, 'password': 0}
    )

    if not candidate_data:
        raise HTTPException(status_code=404, detail='Account not found')
    
    if candidate_data['typeAccount'] != 'Candidate':
        raise HTTPException(status_code=403, detail='Only candidates can apply')

    job_data = await db['jobs'].find_one(
        {'jobId': application.jobId},
        {'_id': 0}
    )
    
    if not job_data:
        raise HTTPException(status_code=404, detail='Job not found')
    
    if job_data['status'] != 'Enabled':
        raise HTTPException(status_code=403, detail='The job is not available')
    
    application_data = application.model_dump()

    application_data['applicationId'] = str(uuid4())

    application_data['candidateId'] = userId
    application_data['candidateName'] = f'{candidate_data['firstName']} {candidate_data['lastName']}'

    application_data['companyId'] = job_data['companyId']
    application_data['companyName'] = job_data['companyName']
    application_data['jobName'] = job_data['jobName']
    application_data['jobPosition'] = job_data['jobPosition']
    application_data['jobSalaryRange'] = job_data['jobSalaryRange']

    application_data['status'] = 'New'

    now_co = datetime.now(ZoneInfo("America/Bogota"))

    application_data['applicationDate'] = now_co

    months = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
        7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }

    application_data['applicationDateStr'] = f'{now_co.day} {months[now_co.month]} {now_co.year}'

    await db['applications'].insert_one(application_data)

    return {'message': 'Application Created'}

async def update_application(req: Request, application: UpdateApplication):
    userId = req.state.user['userId']

    await check_valid_company(userId)

    application_exists = await db['applications'].count_documents(
        {'companyId': userId, 'applicationId': application.applicationId, 'candidateId': application.candidateId}
    )
    if application_exists <= 0:
        raise HTTPException(status_code=403, detail='You cannot update this application')
    
    await db['applications'].update_one(
        {'companyId': userId, 'applicationId': application.applicationId, 'candidateId': application.candidateId},
        {'$set': {'status': application.status, 'statusMessage': application.message}}
    )

    return {'message': 'Application updated'}