from pydantic import BaseModel
from typing import Literal

class CreateApplication(BaseModel):
    jobId: str

class UpdateApplication(BaseModel):
    applicationId: str
    candidateId: str
    status: Literal['In progress', 'To interview', 'Interviewed', 'Refused', 'Contracted']
    message: str | None = None