from fastapi import Request
from uuid import uuid4
from datetime import datetime, timezone

from ..database import db

from .models import CreateInterview
from .functions import check_valid_company, check_valid_applicant

async def schedule(req: Request, interview: CreateInterview):
    companyId = req.state.user["userId"]

    company = await check_valid_company(companyId)
    candidate = await check_valid_applicant(interview.candidateId)

    interview_data = interview.model_dump()
    interview_data["interviewId"] = str(uuid4())
    interview_data["companyId"] = companyId
    interview_data["status"] = "Scheduled"

    interview_data["roomName"] = f"Interview-{uuid4().hex[:12]}"
    interview_data["startTime"] = datetime.strptime(
        f"{interview.date} {interview.time}", "%Y-%m-%d %H:%M"
    ).replace(tzinfo=timezone.utc)

    interview_data["displayNameRecruiter"] = f"{company['firstName'].split[0]} {company['lastName'].split[0]}"
    interview_data["displayNameCandidate"] = f"{candidate['firstName'].split[0]} {candidate['lastName'].split[0]}"

    await db["interviews"].insert_one(interview_data)

    return {"message": "Interview scheduled successfully"}