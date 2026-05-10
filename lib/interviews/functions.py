from fastapi import HTTPException

from ..database import db

async def check_valid_company(companyId: str):
    query = await db["users"].find_one(
        {"userId": companyId},
        {
            "companyName": 1,
            "firstName": 1,
            "lastName": 1,
            "typeAccount": 1
        }
    )

    if not query:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if query["typeAccount"] != "Company":
        raise HTTPException(status_code=403, detail="You are not authorized to perform this action")

    return query

async def check_valid_applicant(candidateId: str):
    query = await db["users"].find_one(
        {"userId": candidateId},
        {
            "firstName": 1,
            "lastName": 1,
            "typeAccount": 1
        }
    )

    if not query:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if query["typeAccount"] != "Candidate":
        raise HTTPException(status_code=403, detail="You can only assign interviews to job applicants.")
    
    return query