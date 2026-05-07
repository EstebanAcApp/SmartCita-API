from pydantic import BaseModel, EmailStr

class RegisterUser(BaseModel):
    email: EmailStr
    firstName: str
    lastName: str
    password: str

class RegisterCompany(BaseModel):
    email: EmailStr
    firstName: str
    lastName: str
    companyName: str
    password: str

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