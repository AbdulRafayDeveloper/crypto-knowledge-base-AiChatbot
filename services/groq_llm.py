from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
load_dotenv()

# Load environment variables
GROQ_API_KEY=os.getenv('GROQ_API_KEY')

# Initialize the LLM

llm = ChatGroq(
    model="llama3-8b-8192",
    temperature=1.0,
    max_tokens=4091,
    api_key=GROQ_API_KEY
)

# llm = ChatOpenAI(
#     api_key=os.getenv('OPENAI_API_KEY'),
#     model="gpt-3.5-turbo"
#     )