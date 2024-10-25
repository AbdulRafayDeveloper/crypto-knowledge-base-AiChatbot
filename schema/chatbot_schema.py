from pydantic import BaseModel
from typing import List

"""
class ChatbotRequest(BaseModel):
    urls: List[str] = ["https://solar-studios.gitbook.io/solar-studios",                  
                       "https://solar-studios.gitbook.io/solar-studios/introduction-welcome-to-solar-studios/solar-dex",
                       "https://solar-studios.gitbook.io/solar-studios/introduction-welcome-to-solar-studios/solar-dominion",
                       "https://solar-studios.gitbook.io/solar-studios/introduction-welcome-to-solar-studios/solar-manga",
                       "https://solar-studios.gitbook.io/solar-studios/get-started/soneium", "https://solar-studios.gitbook.io/solar-studios/get-started/eclipse", "https://solar-studios.gitbook.io/solar-studios/what-is-v3"
                  
                  ]
    query: str
"""
    
    
from pydantic import BaseModel
from typing import List, Optional

# Unified schema for the chatbot requests


# class ChatbotRequest(BaseModel):
#     urls: Optional[List[str]] = [
#         "https://solar-studios.gitbook.io/solar-studios",
#         "https://solar-studios.gitbook.io/solar-studios/introduction-welcome-to-solar-studios/solar-dex",
#         "https://solar-studios.gitbook.io/solar-studios/introduction-welcome-to-solar-studios/solar-dominion",
#         "https://solar-studios.gitbook.io/solar-studios/introduction-welcome-to-solar-studios/solar-manga",
#         "https://solar-studios.gitbook.io/solar-studios/get-started/soneium",
#         "https://solar-studios.gitbook.io/solar-studios/get-started/eclipse",
#         "https://solar-studios.gitbook.io/solar-studios/what-is-v3"
#     ]
#     query: str
#     message: str
class ChatbotRequest(BaseModel):
    message: str = "Loads data from a text file using TextLoader processes it and generates a response to a user query based on the loaded data and tell"


class ChatbotResponse(BaseModel):
    response: str
