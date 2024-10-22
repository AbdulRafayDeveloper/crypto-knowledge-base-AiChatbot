from fastapi import FastAPI
from routers.api import routers
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Initialize the FastAPI app first
app = FastAPI()

# Define the allowed origins (origins where your frontend or other services will run)
origins = [
    "http://localhost:3000",  # React or any other frontend running locally
    "http://localhost:8000",  # Local FastAPI backend
    "https://b8svk58c-8000.inc1.devtunnels.ms/"  # Any other specific frontend URL
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    # You can allow specific origins or use ["*"] to allow all origins
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    # Allow all headers (like Authorization, Content-Type, etc.)
    allow_headers=["*"],
)

# Include your router
app.include_router(routers)

# Entry point for running the FastAPI application
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
