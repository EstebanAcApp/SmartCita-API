from fastapi import HTTPException

from ..database import db

async def check_valid_company(companyId: str):
    query = await db["users"].find_one(
        {"userId": companyId},
        {
            "typeAccount": 1,
            "paymentStatus": 1
        }
    )

    if not query:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if query["typeAccount"] != "Company":
        raise HTTPException(status_code=403, detail="You are not authorized to perform this action")

    if query["paymentStatus"] != "Active":
        raise HTTPException(status_code=403, detail="You are not authorized to perform this action")

async def check_valid_applicant(userId: str):
    query = await db["users"].find_one(
        {"userId": userId},
        {
            "typeAccount": 1,
            "paymentStatus": 1
        }
    )

    if not query:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if query["typeAccount"] != "User":
        raise HTTPException(status_code=403, detail="You can only assign interviews to job applicants.")