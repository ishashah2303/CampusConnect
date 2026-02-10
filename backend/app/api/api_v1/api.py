from fastapi import APIRouter
from app.api.api_v1.endpoints import users, login, events, chat

api_router = APIRouter()

api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(events.router, prefix="/events", tags=["events"])
api_router.include_router(chat.router, tags=["chat"])

@api_router.get("/status")
def status():
    return {"status": "ok"}
