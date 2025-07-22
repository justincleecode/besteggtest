"""
Simple working tests for NYTimes Article Microservice
"""

import pytest
from fastapi.testclient import TestClient
import os

# Set API key before importing the app
os.environ["NYTIMES_API_KEY"] = "test_api_key_for_testing"

from app.main import app

client = TestClient(app)


class TestBasicEndpoints:
    """Basic tests that should always work"""
    
    def test_root_endpoint(self):
        """Test the root endpoint returns correct information"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "NYTimes Article Microservice"
        assert data["version"] == "1.0.0"
        assert "/nytimes/topstories" in data["endpoints"]
        assert "/nytimes/articlesearch" in data["endpoints"]
    
    def test_docs_endpoint(self):
        """Test that OpenAPI docs are available"""
        response = client.get("/docs")
        assert response.status_code == 200
    
    def test_openapi_json(self):
        """Test that OpenAPI JSON schema is available"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert data["info"]["title"] == "NYTimes Article Microservice"
    
    def test_article_search_validation(self):
        """Test validation for article search endpoint"""
        # Missing required query parameter should return 422
        response = client.get("/nytimes/articlesearch")
        assert response.status_code == 422
    
    def test_invalid_endpoint(self):
        """Test handling of invalid endpoints"""
        response = client.get("/invalid/endpoint")
        assert response.status_code == 404


class TestConfiguration:
    """Test configuration and setup"""
    
    def test_api_key_is_set(self):
        """Test that API key is configured"""
        from app.core.config import settings
        assert settings.nytimes_api_key is not None
        assert settings.nytimes_api_key != ""
    
    def test_base_url_configuration(self):
        """Test that base URL is properly configured"""
        from app.core.config import settings
        assert settings.nytimes_base_url == "https://api.nytimes.com/svc"
    
    def test_app_settings(self):
        """Test application settings"""
        from app.core.config import settings
        assert settings.app_name == "NYTimes Article Microservice"
        assert settings.app_version == "1.0.0"


class TestModels:
    """Test Pydantic models"""
    
    def test_top_story_model(self):
        """Test TopStory model creation"""
        from app.models.nytimes import TopStory
        
        story_data = {
            "title": "Test Title",
            "section": "technology",
            "url": "https://example.com",
            "abstract": "Test abstract",
            "published_date": "2024-01-01T10:00:00-05:00"
        }
        
        story = TopStory(**story_data)
        assert story.title == "Test Title"
        assert story.section == "technology"
        assert story.url == "https://example.com"
        assert story.abstract == "Test abstract"
        assert story.published_date == "2024-01-01T10:00:00-05:00"
    
    def test_article_model(self):
        """Test Article model creation"""
        from app.models.nytimes import Article
        
        article_data = {
            "headline": "Test Headline",
            "snippet": "Test snippet",
            "web_url": "https://example.com/article",
            "pub_date": "2024-01-01T10:00:00+0000"
        }
        
        article = Article(**article_data)
        assert article.headline == "Test Headline"
        assert article.snippet == "Test snippet"
        assert article.web_url == "https://example.com/article"
        assert article.pub_date == "2024-01-01T10:00:00+0000"
    
    def test_top_stories_response_model(self):
        """Test TopStoriesResponse model"""
        from app.models.nytimes import TopStoriesResponse, TopStory
        
        story = TopStory(
            title="Test",
            section="tech",
            url="https://example.com",
            abstract="Abstract",
            published_date="2024-01-01T10:00:00-05:00"
        )
        
        response = TopStoriesResponse(stories=[story], total_count=1)
        assert len(response.stories) == 1
        assert response.total_count == 1
        assert response.stories[0].title == "Test"
    
    def test_article_search_response_model(self):
        """Test ArticleSearchResponse model"""
        from app.models.nytimes import ArticleSearchResponse, Article
        
        article = Article(
            headline="Test Headline",
            snippet="Test snippet",
            web_url="https://example.com",
            pub_date="2024-01-01T10:00:00+0000"
        )
        
        response = ArticleSearchResponse(
            articles=[article],
            total_count=1,
            query="test"
        )
        assert len(response.articles) == 1
        assert response.total_count == 1
        assert response.query == "test"
        assert response.articles[0].headline == "Test Headline"


if __name__ == "__main__":
    pytest.main([__file__])
