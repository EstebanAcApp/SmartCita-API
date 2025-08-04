from fastapi.responses import JSONResponse
from lib.database import db
from lib.auth.security import logoutResponse

auth_routes = ("/auth/register/", "/auth/login/", "/auth/mfa/login/")
webhooks_routes = ("/webhooks/stripe/",)

def is_auth_route(path: str) -> bool:
    return any(path.startswith(route) for route in auth_routes)

def is_webhook_route(path: str) -> bool:
    return any(path.startswith(route) for route in webhooks_routes)

def unauthorized(code=401, message="Unauthorized"):
    return JSONResponse(status_code=code, content={"message": message})

async def validate_device(userId: str, deviceId: str):
    userDevice = await db["users"].find_one({"userId": userId, "userDevices.deviceId": deviceId})
    if not userDevice:
        return logoutResponse()