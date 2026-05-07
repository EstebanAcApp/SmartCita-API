from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from dotenv import load_dotenv
load_dotenv()

from middleware.auth import validate_auth
from lib.database import client

from routes.auth import auth_router
from routes.interviews import interview_router
from routes.rooms import room_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    client.close()

app = FastAPI(lifespan=lifespan)

# ✅ Habilita CORS antes de agregar los routers
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://humble-meme-vwgw7x6g5553wqg5-3000.app.github.dev",
        "https://smartcita.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def middleware_auth(req: Request, call_next):
    return await validate_auth(req, call_next)

app.include_router(auth_router)
app.include_router(interview_router)
app.include_router(room_router)