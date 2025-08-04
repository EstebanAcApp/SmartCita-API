from motor.motor_asyncio import AsyncIOMotorClient
from os import getenv

mongodb_uri = getenv("URI_MONGODB")

client = AsyncIOMotorClient(mongodb_uri)
db = client["flowy_hire"]