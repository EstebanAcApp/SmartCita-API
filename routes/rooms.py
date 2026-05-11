from fastapi import APIRouter, Request

from lib.rooms.crud import create_livekit_token, end_livekit_room
from lib.rooms.models import EndRoomModel

room_router = APIRouter()

@room_router.post("/room/{interview_id}/token/")
async def generate_livekit_token(req: Request, interview_id: str):
    return await create_livekit_token(req, interview_id)

@room_router.delete("/room/end/")
async def create_room(req: Request, room: EndRoomModel):
    return await end_livekit_room(req, room)