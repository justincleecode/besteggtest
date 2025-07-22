"""
Configuration settings for the application
"""

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # NYTimes API configuration
    nytimes_api_key: str = os.getenv("NYTIMES_API_KEY", "")
    nytimes_base_url: str = "https://api.nytimes.com/svc"
    
    # Application settings
    app_name: str = "NYTimes Article Microservice"
    app_version: str = "1.0.0"
    
    class Config:
        env_file = ".env"


settings = Settings()

# Validate required settings
if not settings.nytimes_api_key:
    raise ValueError("NYTIMES_API_KEY environment variable is required")
