from pydantic import BaseModel

class EndRoomModel(BaseModel):
    roomName: str
    rating: float
    note: str