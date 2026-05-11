from pydantic import BaseModel

class UpdateDataCandidate(BaseModel):
    firstName: str
    lastName: str
    phoneNumber: str

class UpdateDataCompany(BaseModel):
    firstName: str
    lastName: str
    companyName: str
    companyIndustry: str
    companySize: str
    companyLocation: str
    companyWebsite: str