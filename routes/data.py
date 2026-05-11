from fastapi import APIRouter, Request, File, UploadFile

from lib.data.crud import update_data_candidate, update_cv_candidate, delete_cv_candidate, update_data_company, data
from lib.data.models import UpdateDataCandidate, UpdateDataCompany

data_router = APIRouter()

@data_router.patch("/data/update/candidate/")
async def update_candidate_data_route(req: Request, data: UpdateDataCandidate):
    return await update_data_candidate(req, data)

@data_router.patch("/data/update/candidate/cv/")
async def update_candidate_cv_route(req: Request, cv: UploadFile = File(...)):
    return await update_cv_candidate(req, cv)

@data_router.delete("/data/delete/candidate/cv/")
async def delete_candidate_cv_route(req: Request):
    return await delete_cv_candidate(req)

@data_router.patch("/data/update/company/")
async def update_company_data_route(req: Request, data: UpdateDataCompany):
    return await update_data_company(req, data)

@data_router.get("/data/")
async def user_data(req: Request):
    return await data(req)