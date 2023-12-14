from fastapi import APIRouter

from server.views.chat import conversation_router, conversation_ws_router


router = APIRouter()
ws_routers = APIRouter()
router.include_router(conversation_router)
ws_routers.include_router(conversation_ws_router)
