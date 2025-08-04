from fastapi import APIRouter, Request

from lib.auth.crud import userRegister, companyRegister, loginUser, deviceLogout, logoutUser
from lib.auth.models import RegisterUser, RegisterCompany, Login, LogoutDevice

auth_router = APIRouter()

@auth_router.post("/auth/register/user/", status_code=201)
async def register_user(req: Request, user: RegisterUser):
    return await userRegister(req, user)

@auth_router.post("/auth/register/company/", status_code=201)
async def register_company(req: Request, company: RegisterCompany):
    return await companyRegister(req, company)

@auth_router.post("/auth/login/")
async def login_user(req: Request, user: Login):
    return await loginUser(req, user)

@auth_router.delete("/auth/device/logout/")
async def logout_device_user(req: Request, device: LogoutDevice):
    return await deviceLogout(req, device)

@auth_router.delete("/auth/logout/")
async def logout_user(req: Request):
    return await logoutUser(req)