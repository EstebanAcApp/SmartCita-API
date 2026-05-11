from fastapi import HTTPException, Request

from livekit.api import LiveKitAPI
from livekit.protocol.room import DeleteRoomRequest, CreateRoomRequest
from livekit.api.access_token import AccessToken, VideoGrants

from .models import EndRoomModel

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from os import getenv

from ..database import db

LIVEKIT_API_KEY = getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = getenv("LIVEKIT_API_SECRET")

async def create_livekit_token(req: Request, interview_id: str):
    userId = req.state.user["userId"]

    interview = await db["interviews"].find_one({
        "interviewId": interview_id,
        "$or": [
            {"companyId": userId},
            {"candidateId": userId}
        ]
    })
    if not interview:
        raise HTTPException(status_code=403, detail="You are not allowed to join this interview.")

    if interview["status"] == "Completed":
        raise HTTPException(status_code=403, detail="This interview has already ended.")

    now = datetime.now(ZoneInfo("UTC"))

    start_time = interview["startTime"]
    if start_time.tzinfo is None:
        start_time = start_time.replace(tzinfo=ZoneInfo("UTC"))
    else:
        start_time = start_time.astimezone(ZoneInfo("UTC"))

    if now < (start_time - timedelta(minutes=5)):
        raise HTTPException(status_code=403, detail="Too early to join, please return 5 minutes before the scheduled time.")
    
    if now > (start_time + timedelta(minutes=interview["duration"])):
        raise HTTPException(status_code=403, detail="This interview has already ended due to time constraints.")
        
    if not interview.get("createdRoom", False):
        await create_livekit_room(interview["roomName"])

    if userId == interview["companyId"]:
        identity = interview["displayNameRecruiter"]
    else:
        identity = interview["displayNameCandidate"]

    # 🎫 Crear token
    token = (
        AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
        .with_identity(identity)
        .with_grants(VideoGrants(room_join=True, room=interview["roomName"]))
        .with_ttl(timedelta(minutes=interview["duration"] + 10))
    )

    return {"token": token.to_jwt(), "roomName": interview["roomName"]}

async def create_livekit_room(room_name: str):
    async with LiveKitAPI() as lkapi:
        try:
            await lkapi.room.create_room(CreateRoomRequest(
                name=room_name,
                empty_timeout=2 * 60,  # se elimina 2 min después de que quede vacía
                max_participants=4
            ))
            await db["interviews"].update_one(
                {"roomName": room_name},
                {"$set": {"createdRoom": True, "status": "In progress"}}
            )
        except:
            raise HTTPException(status_code=500, detail="Error creating room")

    return {"message": "Interview room created"}

async def end_livekit_room(req: Request, room: EndRoomModel):
    userId = req.state.user["userId"]

    is_company = await db["interviews"].find_one(
        {"roomName": room.roomName, "companyId": userId}
    )

    if not is_company:
        raise HTTPException(status_code=403, detail="You are not allowed to end this interview.")

    async with LiveKitAPI() as lkapi:
        try:
            await lkapi.room.delete_room(DeleteRoomRequest(
                room=room.roomName,
            ))
            await db["interviews"].update_one(
                {"roomName": room.roomName, "companyId": userId},
                {"$set": {"status": "Completed", 'rating': room.rating, 'note': room.note}}
            )
        except:
            raise HTTPException(status_code=500, detail="Error deleting room")

    return {"message": "Interview room ended and deleted"}