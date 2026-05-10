from fastapi import APIRouter, Request

from lib.applications.crud import create_application, update_application
from lib.applications.models import CreateApplication, UpdateApplication

application_router = APIRouter(prefix='/application')

@application_router.post('/create/', status_code=201)
async def create_application_route(req: Request, application: CreateApplication):
    return await create_application(req, application)

@application_router.patch('/update/', status_code=201)
async def update_application_route(req: Request, application: UpdateApplication):
    return await update_application(req, application)