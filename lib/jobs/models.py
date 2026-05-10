from pydantic import BaseModel
from typing import Literal

class CreateJob(BaseModel):
    jobName: str
    JobDescription: str
    jobPosition: str
    jobModality: Literal['On-Site', 'Remote', 'Hybrid']
    jobCity: str
    jobContract: Literal['Fixed Term', 'Indefinite Term', 'By Work', 'Learning']
    jobSalaryRange: str
    status: Literal['Enabled', 'Disabled']

class UpdateJobStatus(BaseModel):
    jobId: str
    status: Literal['Enabled', 'Disabled']

class DeleteJob(BaseModel):
    jobId: str
    messageConfirmation: str