from fastapi import HTTPException, Request

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
        applications = await db["applications"].find_one(
            {"candidateId": userId},
            {'_id': 0}
        )

        interviews = await db["interviews"].find_one(
            {"candidateId": userId},
            {'_id': 0}
        )
        
        return {
            'user': user,
            'applications': applications,
            'interviews': interviews
        }
    
    if user['typeAccount'] == 'Company':
        jobs = await db["jobs"].find_one(
            {"companyId": userId},
            {'_id': 0}
        )

        interviews = await db["interviews"].find_one(
            {"companyId": userId},
            {'_id': 0}
        )
        
        candidates = await db["applications"].find_one(
            {"companyId": userId},
            {'_id': 0}
        )

        return {
            'user': user,
            'jobs': jobs,
            'interviews': interviews,
            'candidates': candidates
        }