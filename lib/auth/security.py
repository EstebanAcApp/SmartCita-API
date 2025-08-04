from fastapi import Request
from fastapi.responses import JSONResponse
import bcrypt
from uuid import uuid4
from user_agents import parse
from secrets import randbelow
from time import time

from ..tokens_jwt.create import create_access_token

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())

def loginResponse(userId: str, deviceId: str):
    access_token = create_access_token(userId, deviceId)
    TOKEN_MAX_AGE = 30 * 24 * 60 * 60

    response = JSONResponse(content={"message": "Successfully"})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="none",
        path="/",
        max_age=TOKEN_MAX_AGE
    )

    return response

def logoutResponse():
    response = JSONResponse(content={"message": "User logged out successfully"})
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=True,
        samesite="none",
        path="/"
    )

    return response

def get_login_date():
    return int(time())

def get_request_info(req: Request, deviceId: str):
    # IP del cliente (usando Vercel header si aplica)
    ip = req.headers.get("x-forwarded-for", req.client.host).split(",")[0].strip()

    # User-Agent
    user_agent_str = req.headers.get("user-agent", "")
    user_agent = parse(user_agent_str)

    return {
        "deviceId": deviceId,
        "ip": ip,
        "device_family": user_agent.device.family,  # Ej: 'iPhone', 'Other', 'Windows PC'
        "is_mobile": user_agent.is_mobile,
        "is_tablet": user_agent.is_tablet,
        "is_pc": user_agent.is_pc,
        "os": f"{user_agent.os.family} {user_agent.os.version_string}",  # Ej: 'iOS 16.4'
        "browser": f"{user_agent.browser.family} {user_agent.browser.version_string}",  # Ej: 'Chrome 114.0.0'
    }

def generate_mfa_code():
    return str(randbelow(90000) + 10000)