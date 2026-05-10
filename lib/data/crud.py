from fastapi import HTTPException, Request
from datetime import timezone

from ..database import db

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
        
        applications = await cursor_applications.to_list()
        interviews = await cursor_interviews.to_list()

        for interview in interviews:
            if "startTime" in interview and interview["startTime"]:
                interview["startTime"] = interview["startTime"].replace(tzinfo=timezone.utc)

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

        jobs = await cursor_jobs.to_list()
        interviews = await cursor_interviews.to_list()
        candidates = await cursor_candidates.to_list()

        for interview in interviews:
            if "startTime" in interview and interview["startTime"]:
                interview["startTime"] = interview["startTime"].replace(tzinfo=timezone.utc)
                
        return {
            'user': user,
            'jobs': jobs,
            'interviews': interviews,
            'candidates': candidates
        }