from fastapi import APIRouter, Request

from lib.rooms.crud import create_livekit_token, end_livekit_room

room_router = APIRouter()

@room_router.post("/room/{interview_id}/token/")
async def generate_livekit_token(req: Request, interview_id: str):
    return await create_livekit_token(req, interview_id)

@room_router.delete("/room/{roomName}/end/")
async def create_room(req: Request, roomName: str):
    return await end_livekit_room(req, roomName)