from fastapi import APIRouter
from routers.v1 import chatbot_router

routers=APIRouter()
routers.include_router(chatbot_router.router)