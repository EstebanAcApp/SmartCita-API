from pydantic import BaseModel

class CreateInterview(BaseModel):
    candidateId: str
    date: str
    time: str
    duration: int
    description: str
    position: str