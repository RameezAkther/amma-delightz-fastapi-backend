from fastapi import APIRouter, Depends
from schemas.chat import ChatRequest, ChatResponse
from services.chat_service import ChatService
from core.dependencies import get_current_user
from models.user import User

router = APIRouter(prefix="/api/chat", tags=["chat"])

@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest, current_user: User = Depends(get_current_user)):
    return await ChatService.get_chat_response(request.message)
