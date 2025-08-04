from fastapi import HTTPException, Request
from uuid import uuid4

from ..database import db
from .models import RegisterUser, RegisterCompany, Login, MfaLogin, LogoutDevice
from .security import hash_password, verify_password, loginResponse, logoutResponse, get_request_info, generate_mfa_code, get_login_date

async def userRegister(req: Request, user: RegisterUser):
    email = user.email.lower()

    existing_user = await db["users"].find_one({"email": email})
    if existing_user:
        raise HTTPException(status_code=401, detail="Unauthorized Register")

    userId = str(uuid4())
    deviceId = str(uuid4())

    hashed_password = hash_password(user.password)
    user_info = get_request_info(req, deviceId)
    loginDate = get_login_date()
    
    user_dict = user.dict()
    user_dict["userId"] = userId
    user_dict["password"] = hashed_password
    user_dict["userDevices"] = [user_info]
    user_dict["lastLogin"] = loginDate
    user_dict["typeAccount"] = "User"

    await db["users"].insert_one(user_dict)

    return loginResponse(userId, deviceId)


async def companyRegister(req: Request, company: RegisterCompany):
    email = company.email.lower()

    existing_user = await db["users"].find_one({"email": email})
    if existing_user:
        raise HTTPException(status_code=401, detail="Unauthorized Register")

    userId = str(uuid4())
    deviceId = str(uuid4())

    hashed_password = hash_password(company.password)
    user_info = get_request_info(req, deviceId)
    loginDate = get_login_date()
    
    company_dict = company.dict()
    company_dict["userId"] = userId
    company_dict["password"] = hashed_password
    company_dict["userDevices"] = [user_info]
    company_dict["lastLogin"] = loginDate
    company_dict["typeAccount"] = "Company"
    company_dict["paymentStatus"] = "Pending"

    await db["users"].insert_one(company_dict)

    return loginResponse(userId, deviceId)


async def loginUser(req: Request, user: Login):
    email = user.email.lower()

    existing_user = await db["users"].find_one({"email": email})
    if not existing_user:
        raise HTTPException(status_code=401, detail="Unauthorized Login")

    if not verify_password(user.password, existing_user["password"]):
        raise HTTPException(status_code=401, detail="Unauthorized Login")

    deviceId = str(uuid4())
    user_info = get_request_info(req, deviceId)
    
    loginDate = get_login_date()

    await db["users"].update_one(
        {"userId": existing_user["userId"]},
        {
            "$push": {"userDevices": user_info},
            "$set": {"lastLogin": loginDate}
        }
    )

    return loginResponse(existing_user["userId"], deviceId)


async def loginMfa(req: Request, user: MfaLogin):
    email = user.email.lower()

    existing_user = await db["users"].find_one({"email": email})
    if not existing_user:
        raise HTTPException(status_code=401, detail="Unauthorized Login")
    
    if not verify_password(user.password, existing_user["password"]):
        raise HTTPException(status_code=401, detail="Unauthorized Login")
    
    if not existing_user["mfaEnabled"] or not existing_user["mfaCode"]:
        raise HTTPException(status_code=401, detail="Unauthorized Login")
    
    if existing_user.get("mfaAttempts", 0) >= 3:
        raise HTTPException(status_code=401, detail="Too many MFA attempts")
    
    if existing_user["mfaCode"] != user.mfaCode:
        await db["users"].update_one(
            {"userId": existing_user["userId"]},
            {
                "$inc": {"mfaAttempts": 1}
            }
        )
        raise HTTPException(status_code=401, detail="Invalid MFA code")
    
    deviceId = str(uuid4())
    user_info = get_request_info(req, deviceId)
    
    loginDate = get_login_date()

    await db["users"].update_one(
        {"userId": existing_user["userId"]},
        {
            "$push": {"userDevices": user_info},
            "$set": {"lastLogin": loginDate},
            "$unset": {"mfaAttempts": "", "mfaCode": ""}
        }
    )

    return loginResponse(existing_user["userId"], deviceId)


async def deviceLogout(req: Request, device: LogoutDevice):
    userId = req.state.user["userId"]
    deviceId = device.deviceId

    await db["users"].update_one(
        {"userId": userId},
        {"$pull": {"userDevices": {"deviceId": deviceId}}}
    )


async def logoutUser(req: Request):
    userId = req.state.user["userId"]
    deviceId = req.state.user["deviceId"]

    await db["users"].update_one(
        {"userId": userId},
        {"$pull": {"userDevices": {"deviceId": deviceId}}}
    )

    return logoutResponse()


###USER SECURITY###
async def enableMfa(req: Request):
    userId = req.state.user["userId"]
    
    await db["users"].update_one(
        {"userId": userId},
        {"$set": {"mfaEnabled": True}}
    )


async def disableMfa(req: Request):
    userId = req.state.user["userId"]

    await db["users"].update_one(
        {"userId": userId},
        {"$set": {"mfaEnabled": False}}
    )