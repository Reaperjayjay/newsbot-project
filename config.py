from dotenv import load_dotenv
load_dotenv()
import os
import sys
import logging

# Load environment variables
NOTION_TOKEN = os.getenv('NOTION_TOKEN')
DATABASE_ID = os.getenv('DATABASE_ID')  
GNEWS_API_KEY = os.getenv('GNEWS_API_KEY')
MEDIASTACK_API_KEY = os.getenv('MEDIASTACK_API_KEY')
CURRENTS_API_KEY = os.getenv('CURRENTS_API_KEY')

# Request Configuration
REQUEST_TIMEOUT = 30  # seconds
RATE_LIMIT_DELAY = 0.1  # seconds between Notion API calls
MAX_ARTICLES_PER_API = 50  # limit per API to avoid overwhelming

# Notion Property Names
NOTION_PROPERTIES = {
    'headline': 'Headline',
    'source': 'Source',
    'url': 'URL',
    'category': 'Category',
    'published_at': 'Published At',
    'added_at': 'Added At'
}

def setup_logging() -> logging.Logger:
    """Configure core logging with clean formatting."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger("NewsAggregator")