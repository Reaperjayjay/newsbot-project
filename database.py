import time
import logging
from typing import List, Set, Optional, Tuple
from datetime import datetime, timezone
from notion_client import Client

from models import NewsArticle
from config import NOTION_PROPERTIES, RATE_LIMIT_DELAY

class NotionManager:
    """Handles all Notion database infrastructure operations and writes."""
    
    def __init__(self, token: str, database_id: str, logger: logging.Logger):
        self.client = Client(auth=token)
        self.database_id = database_id
        self.logger = logger
        self._existing_titles: Optional[Set[str]] = None
    
    def ensure_database_properties(self) -> bool:
        """Ensure all required properties exist in the Notion database schema."""
        try:
            required_properties = {
                NOTION_PROPERTIES['source']: {
                    "select": {
                        "options": [
                            {"name": "GNews", "color": "blue"},
                            {"name": "MediaStack", "color": "green"}, 
                            {"name": "Currents", "color": "orange"},
                            {"name": "Manual", "color": "gray"},
                            {"name": "Unknown", "color": "default"}
                        ]
                    }
                },
                NOTION_PROPERTIES['url']: {"url": {}},
                NOTION_PROPERTIES['category']: {
                    "select": {
                        "options": [
                            {"name": "General", "color": "default"},
                            {"name": "Sports", "color": "green"},
                            {"name": "Politics", "color": "red"},
                            {"name": "Business", "color": "blue"},
                            {"name": "Technology", "color": "purple"},
                            {"name": "Entertainment", "color": "pink"},
                            {"name": "Health", "color": "yellow"}
                        ]
                    }
                },
                NOTION_PROPERTIES['published_at']: {"date": {}},
                NOTION_PROPERTIES['added_at']: {"date": {}}
            }
            
            database = self.client.databases.retrieve(self.database_id)
            
            # Safe Parsing: Handles standard dictionaries, custom SDK objects, or dot notation structures
            if hasattr(database, "get"):
                current_properties = database.get("properties", {})
            elif isinstance(database, dict):
                current_properties = database.get("properties", {})
            else:
                current_properties = getattr(database, "properties", {})
                
            if not current_properties:
                self.logger.error("Could not find a valid properties schema in the Notion response payload.")
                return False
            
            missing_properties = {}
            for prop_name, prop_schema in required_properties.items():
                if prop_name not in current_properties:
                    missing_properties[prop_name] = prop_schema
            
            if missing_properties:
                self.client.databases.update(
                    self.database_id,
                    properties=missing_properties
                )
                self.logger.info(f"Added missing properties: {', '.join(missing_properties.keys())}")
            else:
                self.logger.info("All required database properties verified")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to verify database schema: {e}")
            return False
    
    def get_existing_headlines(self) -> Set[str]:
        """Fetch all existing headlines from Notion to prevent duplication."""
        if self._existing_titles is not None:
            return self._existing_titles
        
        existing_titles = set()
        try:
            has_more = True
            start_cursor = None
            
            while has_more:
                query_params = {"database_id": self.database_id}
                if start_cursor:
                    query_params["start_cursor"] = start_cursor
                
                response = self.client.databases.query(**query_params)
                
                # Check properties inside the query results safely
                results = response.get("results", []) if hasattr(response, "get") else getattr(response, "results", [])
                
                for page in results:
                    page_props = page.get("properties", {}) if isinstance(page, dict) else getattr(page, "properties", {})
                    title_data = page_props.get(NOTION_PROPERTIES['headline'], {}).get("title", [])
                    
                    if title_data:
                        title = title_data[0]["text"]["content"].strip()
                        if title:
                            existing_titles.add(title)
                
                has_more = response.get("has_more", False) if hasattr(response, "get") else getattr(response, "has_more", False)
                start_cursor = response.get("next_cursor", None) if hasattr(response, "get") else getattr(response, "next_cursor", None)
            
            self._existing_titles = existing_titles
            self.logger.info(f"Retrieved {len(existing_titles)} existing headlines from Notion")
            return existing_titles
            
        except Exception as e:
            self.logger.error(f"Error fetching existing headlines: {e}")
            return set()
    
    def add_articles(self, articles: List[NewsArticle]) -> Tuple[int, int, int]:
        """Process and commit a batch of articles into Notion."""
        if not articles:
            self.logger.warning("No articles to process for database insertion")
            return 0, 0, 0
        
        existing_headlines = self.get_existing_headlines()
        added_count = skipped_count = error_count = 0
        
        for article in articles:
            try:
                if not article.is_valid:
                    self.logger.warning(f"Skipped invalid article structure: {article.title}")
                    skipped_count += 1
                    continue
                
                if article.title in existing_headlines:
                    self.logger.info(f"Skipped duplicate record: {article.title}")
                    skipped_count += 1
                    continue
                
                self._create_notion_page(article)
                self.logger.info(f"Successfully added record: {article.title}")
                added_count += 1
                
                existing_headlines.add(article.title)
                time.sleep(RATE_LIMIT_DELAY)
                
            except Exception as e:
                self.logger.error(f"Error executing commit for item '{article.title}': {e}")
                error_count += 1
                continue
        
        return added_count, skipped_count, error_count
    
    def _create_notion_page(self, article: NewsArticle) -> None:
        """Map object attributes to Notion's explicit property payload formatting."""
        current_time = datetime.now(timezone.utc).isoformat()
        safe_source = self._validate_select_option(article.source, "source")
        safe_category = self._validate_select_option(article.category, "category")
        
        properties = {
            NOTION_PROPERTIES['headline']: {"title": [{"text": {"content": article.title}}]},
            NOTION_PROPERTIES['source']: {"select": {"name": safe_source}},
            NOTION_PROPERTIES['url']: {"url": article.url},
            NOTION_PROPERTIES['category']: {"select": {"name": safe_category}},
            NOTION_PROPERTIES['published_at']: {"date": {"start": article.published_at}},
            NOTION_PROPERTIES['added_at']: {"date": {"start": current_time}}
        }
        
        self.client.pages.create(
            parent={"database_id": self.database_id},
            properties=properties
        )
    
    def _validate_select_option(self, value: str, field_type: str) -> str:
        """Enforce alignment with setup multi-select property options."""
        valid_sources = {"GNews", "MediaStack", "Currents", "Manual", "Unknown"}
        valid_categories = {"General", "Sports", "Politics", "Business", "Technology", "Entertainment", "Health"}
        
        if field_type == "source":
            return value if value in valid_sources else "Unknown"
        elif field_type == "category":
            return value if value in valid_categories else "General"
        return value