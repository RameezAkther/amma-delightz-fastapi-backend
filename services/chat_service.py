from google import genai
from config import settings
from schemas.chat import ChatResponse

class ChatService:
    @staticmethod
    async def get_chat_response(message: str) -> ChatResponse:
        if not settings.gemini_api_key or settings.gemini_api_key in ["YOUR_GEMINI_API_KEY", ""]:
            return ChatResponse(response="Gemini API Key is not configured properly.")
            
        client = genai.Client(api_key=settings.gemini_api_key)
        
        # simple generation, this can be expanded based on the original Spring Boot implementation
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=message
        )
        return ChatResponse(response=response.text)
