from fastapi import Request

from os import getenv
import jwt

from .functions import is_webhook_route, is_auth_route, unauthorized, validate_device

async def validate_auth(req: Request, call_next):
    # ✅ Permitir preflight sin autenticación
    if req.method == "OPTIONS":
        return await call_next(req)

    if is_webhook_route(req.url.path):
        return await call_next(req)

    token = req.cookies.get("access_token")
    secret_key = getenv("SECRET_JWT")

    if is_auth_route(req.url.path) and token:
        return unauthorized(code=403, message="Already authenticated")

    if is_auth_route(req.url.path) and not token:
        return await call_next(req)
    
    if not token:
        return unauthorized()
    
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        req.state.user = payload
    except jwt.InvalidTokenError:
        return unauthorized()
    
    device_check = await validate_device(payload["userId"], payload["deviceId"])
    if device_check:
        return device_check

    return await call_next(req)