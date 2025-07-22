"""
Pytest configuration and fixtures for NYTimes Article Microservice tests
"""

import pytest
import os
from unittest.mock import MagicMock
from fastapi.testclient import TestClient

# Set test environment variables before any imports
os.environ["NYTIMES_API_KEY"] = "test_api_key_for_testing"


@pytest.fixture(scope="session")
def test_client():
    """Create a test client for the FastAPI application"""
    from app.main import app
    return TestClient(app)


@pytest.fixture
def mock_nytimes_response():
    """Fixture for mock NYTimes API response"""
    return {
        "results": [
            {
                "title": "Test Article",
                "section": "technology",
                "url": "https://example.com/test",
                "abstract": "Test abstract",
                "published_date": "2024-01-01T10:00:00-05:00"
            }
        ]
    }


@pytest.fixture
def mock_search_response():
    """Fixture for mock article search response"""
    return {
        "response": {
            "docs": [
                {
                    "headline": {"main": "Test Headline"},
                    "snippet": "Test snippet",
                    "web_url": "https://example.com/article",
                    "pub_date": "2024-01-01T10:00:00+0000"
                }
            ]
        }
    }


@pytest.fixture
def mock_http_client():
    """Fixture for mock HTTP client"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None
    
    mock_client = MagicMock()
    mock_client.get.return_value = mock_response
    
    return mock_client, mock_response


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Automatically set up test environment for each test"""
    # Ensure test API key is set
    original_api_key = os.environ.get("NYTIMES_API_KEY")
    os.environ["NYTIMES_API_KEY"] = "test_api_key_for_testing"
    
    yield
    
    # Restore original API key if it existed
    if original_api_key:
        os.environ["NYTIMES_API_KEY"] = original_api_key
    else:
        os.environ.pop("NYTIMES_API_KEY", None)


# Pytest configuration
def pytest_configure(config):
    """Configure pytest settings"""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as unit test"
    )
    config.addinivalue_line(
        "markers", "performance: mark test as performance test"
    )
