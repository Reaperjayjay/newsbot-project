from typing import Optional
from dataclasses import dataclass
from urllib.parse import urlparse
from datetime import datetime, timezone

@dataclass
class NewsArticle:
    """Data class for standardized news article representation."""
    title: str
    source: str
    url: str
    category: str = "General"
    published_at: Optional[str] = None
    
    def __post_init__(self):
        """Validate and normalize article data."""
        self.title = self.title.strip() if self.title else "No Title"
        self.source = self.source.strip() if self.source else "Unknown"
        self.url = self.url.strip() if self.url else ""
        self.category = self.category.strip() if self.category else "General"
        
        if not self.published_at:
            self.published_at = datetime.now(timezone.utc).isoformat()
    
    @property
    def is_valid(self) -> bool:
        """Check if article has minimum required data."""
        return (
            bool(self.title) and 
            self.title != "No Title" and
            bool(self.url) and
            self._is_valid_url(self.url)
        )
    
    def _is_valid_url(self, url: str) -> bool:
        """Validate URL schema and netloc."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False