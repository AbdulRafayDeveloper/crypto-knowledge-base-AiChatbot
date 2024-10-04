from fastapi import APIRouter, HTTPException, status
from services.chatbot_services import Application
from schema.chatbot_schema import ChatbotRequest

router = APIRouter(
    prefix="/chatbot",
    tags=["chatbot"],
)


@router.post("/generate_response", status_code=status.HTTP_200_OK)
async def generate_response(request: ChatbotRequest):
    try:
        # Validate URL and Query inputs before processing
        if not request.url or not request.query:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid input: URL and query are required."
            )

        # Initialize the Application class with the given URL
        app = Application(request.url)

        # Generate the response using the query
        response = app.run(request.query)

        # If response is empty or invalid, return an appropriate status
        if not response:
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
                detail="No response generated from the LLM."
            )

        # Return the response with a 200 status code
        return {"response": response}

    except HTTPException as e:
        # Let HTTPExceptions pass through to be handled by FastAPI
        raise e

    except Exception as e:
        # Catch any unexpected errors and return a 500 status code
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
