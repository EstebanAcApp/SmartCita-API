from pydantic import BaseModel, EmailStr
from typing import Literal, Optional, List

class RegisterUser(BaseModel):
    email: EmailStr
    password: str
    firstName: str
    lastName: str
    phoneNumber: str
    photoUrl: Optional[str] = None
    workMode: Literal["Remote", "Onsite", "Hybrid"]
    experienceLevel: Literal["Internship", "Junior", "Mid", "Senior", "Lead"]
    jobInterests: List[str]
    resumeUrl: Optional[str] = None

class RegisterCompany(BaseModel):
    email: EmailStr
    password: str
    companyLogoUrl: Optional[str] = None
    companyName: str
    companyDescription: str
    phoneNumber: str
    sector: Literal[
        "Technology", "Healthcare", "Education", "Retail", "Finance", 
        "Hospitality", "Construction", "Manufacturing", "Logistics", "Other"
    ]
    companySize: Literal["1-10", "11-50", "51-200", "201-500", "500+"]
    website: Optional[str] = None
    plan: Literal["Starter", "Growth", "Pro"]

class Login(BaseModel):
    email: EmailStr
    password: str

class LogoutDevice(BaseModel):
    deviceId: str

###AUTH MFA###
class MfaLogin(BaseModel):
    email: EmailStr
    password: str
    mfaCode: str