from fastapi import APIRouter, HTTPException, status
from schema.chatbot_schema import ChatbotRequest, ChatbotResponse
from services.prompts import prompt
from services.api_chatbot import llm_with_tools, tools
from services.chatbot_services import Application
from langchain.agents import AgentExecutor, create_tool_calling_agent

# Create the agent and executor for handling AI responses
agents = create_tool_calling_agent(llm_with_tools, tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agents, tools=tools, verbose=True)

# Create a router for chatbot interactions
router = APIRouter(
    prefix="/chatbot",
    tags=["Chatbot"],
)


@router.post("/", response_model=ChatbotResponse)
async def chat(request: ChatbotRequest):
    try:
        if request.query == "Web-Scraping":
            # Validate that URLs are provided
            if not request.urls:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid input: URLs are required for web scraping."
                )

            # Initialize the Application class with the given list of URLs
            app_instance = Application(request.urls)

            # Generate the response using the message
            response = app_instance.process_and_respond(request.message)

            # If response is empty or invalid, return an appropriate status
            if not response:
                raise HTTPException(
                    status_code=status.HTTP_204_NO_CONTENT,
                    detail="No response generated from the LLM."
                )

            return ChatbotResponse(response=response)

        elif request.query == "Check Balance":
            # Handle Ethereum balance check request
            ai_message = agent_executor.invoke({"input": request.message})

            # Ensure the response is a string or a dictionary with 'output'
            if isinstance(ai_message, dict) and 'output' in ai_message:
                response_str = ai_message['output']
            elif isinstance(ai_message, str):
                response_str = ai_message
            else:
                raise ValueError(
                    "Unexpected response format from agent_executor")

            return ChatbotResponse(response=response_str)

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid query: Expected 'Web-Scraping' or 'Check Balance'."
            )

    except HTTPException as e:
        # Propagate HTTPExceptions
        raise e

    except Exception as e:
        # Handle unexpected errors and return a 500 status code
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
