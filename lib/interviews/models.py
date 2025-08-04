from pydantic import BaseModel

class CreateInterview(BaseModel):
    applicantId: str
    firstName: str
    lastName: str
    date: str
    time: str
    duration: int
    description: str
    interviewType: str