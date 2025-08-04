import jwt
from datetime import datetime, timedelta, timezone

from os import getenv

def create_access_token(userId: str, deviceId: str):
    expiration = datetime.now(tz=timezone.utc) + timedelta(days=30)
    secret_key = getenv("SECRET_JWT")
    
    payload = {
        "userId": userId,
        "deviceId": deviceId,
        "type": "access",
        "exp": expiration
    }

    return jwt.encode(payload, secret_key, algorithm="HS256")