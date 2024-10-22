from fastapi import APIRouter, HTTPException, status
from schema.chatbot_schema import ChatbotRequest, ChatbotResponse
from services.prompts import prompt
from services.api_chatbot import llm_with_tools, tools
from langchain.agents import AgentExecutor, create_tool_calling_agent

# Create the agent and executor for handling AI responses
agents = create_tool_calling_agent(llm_with_tools, tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agents, tools=tools, verbose=True)

# Memory class for storing conversation context


class ChatbotMemory:
    def __init__(self):
        self.history = []

    def add_message(self, user_message, bot_response):
        self.history.append({"user": user_message, "bot": bot_response})

    def get_context(self):
        # Retrieve the last 5 interactions for context (you can adjust this)
        if not self.history:
            return ""
        return " ".join([f"User: {item['user']} Bot: {item['bot']}" for item in self.history])

    def clear_memory(self):
        self.history.clear()


# Create a router for chatbot interactions
router = APIRouter(
    prefix="/chatbot",
    tags=["Chatbot"],
)
memory = ChatbotMemory()


@router.post("/", response_model=ChatbotResponse)
async def chat(request: ChatbotRequest):
    try:
        # Retrieve conversation context
        context = memory.get_context()
        user_input = f"Context: {context} User: {request.message}" if context else request.message

        # Invoke the agent executor to handle the AI response
        result = agent_executor.invoke({"input": user_input})

        # Debug print statement for checking the result
        print(f"Working from routers: {result}")

        # Ensure the response is a string or a dictionary with 'output'
        if isinstance(result, dict) and 'output' in result:
            response_str = result['output']
        elif isinstance(result, str):
            response_str = result
        else:
            raise ValueError("Unexpected response format from agent_executor")

        # Add the current interaction to memory
        memory.add_message(request.message, response_str)
        memory.get_context()

        # Return the response to the FastAPI endpoint
        return ChatbotResponse(response=response_str)

    except HTTPException as e:
        # Propagate HTTPExceptions
        raise e

    except Exception as e:
        # Handle unexpected errors and return a 500 status code
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
