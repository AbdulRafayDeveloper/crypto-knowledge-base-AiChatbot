from pydantic import BaseModel
class ChatbotRequest(BaseModel):
    url: str = "https://solar-studios.gitbook.io/solar-studios"
    query: str
