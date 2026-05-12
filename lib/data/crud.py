from fastapi import Request, HTTPException, UploadFile
from datetime import timezone

from .models import UpdateDataCandidate, UpdateDataCompany

from ..interviews.functions import check_valid_applicant, check_valid_company
from ..s3.functions import upload_cv, delete_cv, get_presigned_url

from ..database import db

async def update_data_candidate(req: Request, data: UpdateDataCandidate):
    userId = req.state.user['userId']

    await check_valid_applicant(userId)

    data_dict = data.model_dump()

    await db['users'].update_one(
        {'userId': userId},
        {'$set': data_dict}
    )

    return {'message': 'Candidate data updated'}

async def update_cv_candidate(req: Request, cv: UploadFile):
    userId = req.state.user['userId']

    await check_valid_applicant(userId)

    if not cv.filename or not cv.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail='Only the .pdf format is valid')

    s3_cv_key = await upload_cv(userId, cv)

    await db['users'].update_one(
        {'userId': userId},
        {'$set': {'cvS3Key': s3_cv_key}}
    )

    return {'message': 'CV updated'}

async def delete_cv_candidate(req: Request):
    userId = req.state.user['userId']

    user_data = await check_valid_applicant(userId)

    await delete_cv(user_data['cvS3Key'])

    await db['users'].update_one(
        {'userId': userId},
        {'$set': {'cvS3Key': None}}
    )

    return {'message': 'CV deleted'}

async def update_data_company(req: Request, data: UpdateDataCompany):
    userId = req.state.user['userId']

    await check_valid_company(userId)

    data_dict = data.model_dump()

    await db['users'].update_one(
        {'userId': userId},
        {'$set': data_dict}
    )

    return {'message': 'Company data updated'}

async def data(req: Request):
    userId = req.state.user["userId"]

    user = await db["users"].find_one(
        {"userId": userId},
        {"password": 0, "_id": 0}
    )
    if not user:
        raise HTTPException(status_code=401, detail="Something Wrong")

    if user['typeAccount'] == 'Candidate':
        cursor_applications = db["applications"].find(
            {"candidateId": userId},
            {'_id': 0}
        )

        cursor_interviews = db["interviews"].find(
            {"candidateId": userId},
            {'_id': 0}
        )
        
        applications = await cursor_applications.to_list(length=1000)
        interviews = await cursor_interviews.to_list(length=1000)

        for interview in interviews:
            if "startTime" in interview and interview["startTime"]:
                interview["startTime"] = interview["startTime"].replace(tzinfo=timezone.utc)

        if user['cvS3Key']:
            user['cvUrl'] = await get_presigned_url(user['cvS3Key'])
        else:
            user['cvUrl'] = None

        return {
            'user': user,
            'applications': applications,
            'interviews': interviews
        }
    
    if user['typeAccount'] == 'Company':
        cursor_jobs = db["jobs"].find(
            {"companyId": userId},
            {'_id': 0}
        )

        cursor_interviews = db["interviews"].find(
            {"companyId": userId},
            {'_id': 0}
        )
        
        cursor_candidates = db["applications"].find(
            {"companyId": userId},
            {'_id': 0}
        )

        jobs = await cursor_jobs.to_list(length=1000)
        interviews = await cursor_interviews.to_list(length=1000)
        candidates = await cursor_candidates.to_list(length=1000)

        for interview in interviews:
            if "startTime" in interview and interview["startTime"]:
                interview["startTime"] = interview["startTime"].replace(tzinfo=timezone.utc)

        for candidate in candidates:
            if "cvS3Key" in candidate and candidate["cvS3Key"]:
                candidate['cvUrl'] = await get_presigned_url(candidate['cvS3Key'])
            else:
                candidate['cvUrl'] = None

        return {
            'user': user,
            'jobs': jobs,
            'interviews': interviews,
            'candidates': candidates
        }