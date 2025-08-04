from fastapi import APIRouter, Request

from lib.interviews.crud import schedule
from lib.interviews.models import CreateInterview

interview_router = APIRouter(prefix="/interviews")

@interview_router.post("/schedule/")
async def schedule_interview(req: Request, interview: CreateInterview):
    return await schedule(req, interview)