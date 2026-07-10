import logging
import requests
from typing import List, Dict, Optional

from models import NewsArticle
from config import REQUEST_TIMEOUT, MAX_ARTICLES_PER_API

class NewsAPIClient:
    """Base network abstraction for interacting with third-party HTTP endpoints."""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.session = requests.Session()
        self.session.timeout = REQUEST_TIMEOUT
    
    def _make_request(self, url: str, api_name: str) -> Optional[Dict]:
        try:
            response = self.session.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            self.logger.error(f"Client Timeout encountered for API: {api_name}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Transport Network error for API {api_name}: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected processing fault for API {api_name}: {e}")
        return None

class GNewsClient(NewsAPIClient):
    """Integration implementation client wrapper targeting GNews endpoints.""" 
    
    def __init__(self, api_key: str, logger: logging.Logger):
        super().__init__(logger)
        self.api_key = api_key
    
    def fetch_articles(self) -> List[NewsArticle]:
        if not self.api_key:
            self.logger.error("GNews configuration missing authentication tokens")
            return []
            
        url = f"https://gnews.io/api/v4/top-headlines?country=ng&lang=en&token={self.api_key}&max={MAX_ARTICLES_PER_API}"
        self.logger.info("Initializing transport stream request to GNews...")
        
        data = self._make_request(url, "GNews")
        if not data or "articles" not in data:
            self.logger.warning("Empty response array payload parsed from GNews")
            return []
        
        articles = []
        for item in data.get("articles", []):
            try:
                article = NewsArticle(
                    title=item.get("title", "No Title"),
                    source="GNews",  
                    url=item.get("url", ""),
                    category="General",  
                    published_at=item.get("publishedAt")
                )
                articles.append(article)
            except Exception as e:
                self.logger.warning(f"Error parsing GNews document entity context structural fields: {e}")
                continue
        
        self.logger.info(f"GNews parser processed {len(articles)} validated node models")
        return articles

class MediaStackClient(NewsAPIClient):
    """Integration implementation client wrapper targeting MediaStack endpoints."""
    
    def __init__(self, api_key: str, logger: logging.Logger):
        super().__init__(logger)
        self.api_key = api_key
    
    def fetch_articles(self) -> List[NewsArticle]:
        if not self.api_key:
            self.logger.error("MediaStack configuration missing authentication tokens")
            return []
            
        url = f"http://api.mediastack.com/v1/news?access_key={self.api_key}&countries=ng&languages=en&limit={MAX_ARTICLES_PER_API}"
        self.logger.info("Initializing transport stream request to MediaStack...")
        
        data = self._make_request(url, "MediaStack")
        if not data or "data" not in data:
            self.logger.warning("Empty response array payload parsed from MediaStack")
            return []
        
        articles = []
        for item in data.get("data", []):
            try:
                category = self._map_category(item.get("category", "General"))
                article = NewsArticle(
                    title=item.get("title", "No Title"),
                    source="MediaStack",  
                    url=item.get("url", ""),
                    category=category,
                    published_at=item.get("published_at")
                )
                articles.append(article)
            except Exception as e:
                self.logger.warning(f"Error parsing MediaStack document entity context structural fields: {e}")
                continue
        
        self.logger.info(f"MediaStack parser processed {len(articles)} validated node models")
        return articles
    
    def _map_category(self, category: str) -> str:
        category_mapping = {
            "sports": "Sports", "politics": "Politics", "business": "Business",
            "technology": "Technology", "tech": "Technology", "entertainment": "Entertainment", "health": "Health"
        }
        return category_mapping.get(category.lower(), "General")

class CurrentsClient(NewsAPIClient):
    """Integration implementation client wrapper targeting Currents endpoints."""
    
    def __init__(self, api_key: str, logger: logging.Logger):
        super().__init__(logger)
        self.api_key = api_key
    
    def fetch_articles(self) -> List[NewsArticle]:
        if not self.api_key:
            self.logger.error("Currents configuration missing authentication tokens")
            return []
            
        url = f"https://api.currentsapi.services/v1/latest-news?apiKey={self.api_key}&language=en&region=ng"
        self.logger.info("Initializing transport stream request to Currents...")
        
        data = self._make_request(url, "Currents")
        if not data or "news" not in data:
            self.logger.warning("Empty response array payload parsed from Currents")
            return []
        
        articles = []
        for item in data.get("news", []):
            try:
                category = self._map_category(item.get("category", "General"))
                article = NewsArticle(
                    title=item.get("title", "No Title"),
                    source="Currents",  
                    url=item.get("url", ""),
                    category=category,
                    published_at=item.get("published")
                )
                articles.append(article)
            except Exception as e:
                self.logger.warning(f"Error parsing Currents document entity context structural fields: {e}")
                continue
        
        self.logger.info(f"Currents parser processed {len(articles)} validated node models")
        return articles
    
    def _map_category(self, category: str) -> str:
        if not category:
            return "General"
        category_mapping = {
            "sports": "Sports", "politics": "Politics", "business": "Business",
            "technology": "Technology", "tech": "Technology", "entertainment": "Entertainment", "health": "Health"
        }
        return category_mapping.get(category.lower(), "General")