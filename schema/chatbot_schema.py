from pydantic import BaseModel
class ChatbotRequest(BaseModel):
    url: str
    query: str
