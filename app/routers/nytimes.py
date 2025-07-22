"""
NYTimes API router with endpoints for top stories and article search
"""

from fastapi import APIRouter, HTTPException, Query
import httpx
from typing import Optional

from app.core.config import settings
from app.models.nytimes import TopStoriesResponse, ArticleSearchResponse, TopStory, Article

router = APIRouter()


@router.get("/topstories", response_model=TopStoriesResponse)
async def get_top_stories():
    """
    Get the two most recent top stories from each category: arts, food, movies, travel, and science
    """
    categories = ["arts", "food", "movies", "travel", "science"]
    all_stories = []
    
    async with httpx.AsyncClient() as client:
        for category in categories:
            try:
                url = f"{settings.nytimes_base_url}/topstories/v2/{category}.json"
                params = {"api-key": settings.nytimes_api_key}
                
                response = await client.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                stories = data.get("results", [])
                
                # Get the two most recent stories from this category
                recent_stories = stories[:2]
                
                for story in recent_stories:
                    top_story = TopStory(
                        title=story.get("title", ""),
                        section=story.get("section", ""),
                        url=story.get("url", ""),
                        abstract=story.get("abstract", ""),
                        published_date=story.get("published_date", "")
                    )
                    all_stories.append(top_story)
                    
            except httpx.HTTPError as e:
                raise HTTPException(
                    status_code=500, 
                    detail=f"Error fetching stories for category {category}: {str(e)}"
                )
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Unexpected error for category {category}: {str(e)}"
                )
    
    return TopStoriesResponse(stories=all_stories, total_count=len(all_stories))


@router.get("/articlesearch", response_model=ArticleSearchResponse)
async def search_articles(
    q: str = Query(..., description="Search query keyword"),
    begin_date: Optional[str] = Query(None, description="Begin date (YYYYMMDD format)"),
    end_date: Optional[str] = Query(None, description="End date (YYYYMMDD format)")
):
    """
    Search NYTimes articles using the Article Search API
    """
    async with httpx.AsyncClient() as client:
        try:
            url = f"{settings.nytimes_base_url}/search/v2/articlesearch.json"
            params = {
                "api-key": settings.nytimes_api_key,
                "q": q
            }
            
            if begin_date:
                params["begin_date"] = begin_date
            if end_date:
                params["end_date"] = end_date
            
            response = await client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            docs = data.get("response", {}).get("docs", [])
            
            articles = []
            for doc in docs:
                headline = doc.get("headline", {}).get("main", "")
                article = Article(
                    headline=headline,
                    snippet=doc.get("snippet", ""),
                    web_url=doc.get("web_url", ""),
                    pub_date=doc.get("pub_date", "")
                )
                articles.append(article)
            
            return ArticleSearchResponse(
                articles=articles, 
                total_count=len(articles),
                query=q
            )
            
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error searching articles: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error: {str(e)}"
            )
