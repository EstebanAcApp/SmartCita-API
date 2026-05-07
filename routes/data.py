from fastapi import APIRouter, Request

from lib.data.crud import data

data_router = APIRouter()

@data_router.get("/data/")
async def user_data(req: Request):
    return await data(req)