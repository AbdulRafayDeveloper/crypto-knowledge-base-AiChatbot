from pydantic import BaseModel
from typing import List
class ChatbotRequest(BaseModel):
    urls: List[str] = ["https://solar-studios.gitbook.io/solar-studios",
                       "https://solar-studios.gitbook.io/solar-studios/introduction-welcome-to-solar-studios/solar-dex",
                       "https://solar-studios.gitbook.io/solar-studios/introduction-welcome-to-solar-studios/solar-dominion",
                       "https://solar-studios.gitbook.io/solar-studios/introduction-welcome-to-solar-studios/solar-manga",
                       "https://solar-studios.gitbook.io/solar-studios/get-started/soneium", "https://solar-studios.gitbook.io/solar-studios/get-started/eclipse", "https://solar-studios.gitbook.io/solar-studios/what-is-v3"
                  
                  ]
    query: str
