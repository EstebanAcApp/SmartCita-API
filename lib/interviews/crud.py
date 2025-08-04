from fastapi import HTTPException, Request
from uuid import uuid4
from datetime import datetime, timezone

from ..database import db

from .models import CreateInterview
from .functions import check_valid_company, check_valid_applicant

async def schedule(req: Request, interview: CreateInterview):
    companyId = req.state.user["userId"]

    await check_valid_company(companyId)
    await check_valid_applicant(interview.applicantId)

    interview_data = interview.dict()
    interview_data["interviewId"] = str(uuid4())
    interview_data["companyId"] = companyId
    interview_data["status"] = "Scheduled"

    # 🔹 Agregar room name único y fecha completa
    interview_data["roomName"] = f"interview-{uuid4().hex[:12]}"
    interview_data["startTime"] = datetime.strptime(
        f"{interview.date} {interview.time}", "%Y-%m-%d %H:%M"
    ).replace(tzinfo=timezone.utc)

    await db["interviews"].insert_one(interview_data)

    return {"message": "Interview scheduled successfully"}