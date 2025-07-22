"""
NYTimes Article Microservice
A FastAPI microservice that integrates with NYTimes APIs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from app.routers import nytimes
from app.core.config import settings

# Load environment variables
load_dotenv()

app = FastAPI(
    title="NYTimes Article Microservice",
    description="A microservice that integrates with NYTimes Top Stories and Article Search APIs",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(nytimes.router, prefix="/nytimes", tags=["nytimes"])


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "NYTimes Article Microservice",
        "version": "1.0.0",
        "endpoints": [
            "/nytimes/topstories",
            "/nytimes/articlesearch"
        ],
        "documentation": "/docs"
    }
