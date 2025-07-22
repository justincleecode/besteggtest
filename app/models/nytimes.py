"""
Pydantic models for NYTimes API request and response validation
"""

from pydantic import BaseModel
from typing import List


class TopStory(BaseModel):
    """Model for a single top story"""
    title: str
    section: str
    url: str
    abstract: str
    published_date: str


class TopStoriesResponse(BaseModel):
    """Response model for top stories endpoint"""
    stories: List[TopStory]
    total_count: int


class Article(BaseModel):
    """Model for a single article from search"""
    headline: str
    snippet: str
    web_url: str
    pub_date: str


class ArticleSearchResponse(BaseModel):
    """Response model for article search endpoint"""
    articles: List[Article]
    total_count: int
    query: str
