Python news engine

A Python-based news aggregation and automation tool that collects articles from multiple news providers, standardizes the data, filters duplicate content, and automatically stores curated news in a Notion database for research, knowledge management, and content planning.

---

## Overview

AI NewsBot is designed to automate the process of collecting and organizing news from multiple online sources. Instead of manually browsing different news websites, the application retrieves articles from several APIs, processes them into a unified format, and uploads them into a structured Notion database.

The project demonstrates backend automation, API integration, object-oriented programming, data processing, and knowledge management using Python.

---

## Features

### Multi-Source News Aggregation

Collects news from multiple providers including:

- GNews
- MediaStack
- Currents
- Additional news APIs (configurable)

Articles from different providers are normalized into a consistent format before further processing.

---

### Notion Integration

Automatically uploads news articles into a Notion database.

Each record contains information such as:

- Title
- Source
- URL
- Description
- Publication Date
- Import Timestamp

---

### Data Normalization

Since every news API returns different JSON structures, the application converts them into a unified article model, making the rest of the application independent of the data source.

---

### Duplicate Detection

Prevents duplicate articles from being inserted into the Notion database by comparing incoming articles against existing records.

---

### Modular Architecture

The application separates responsibilities into dedicated modules, making it easy to maintain and extend.

Modules include:

- Configuration Management
- News API Clients
- Data Models
- Notion Database Operations
- Aggregation Engine

---

### Logging

Implements structured logging to monitor:

- API requests
- Processing steps
- Database operations
- Errors
- Successful imports

---

## System Architecture

```text
                  +----------------+
                  |  News Sources  |
                  +----------------+
                   |      |      |
                   |      |      |
                GNews MediaStack Currents
                   \      |      /
                    \     |     /
                     \    |    /
                      ▼   ▼   ▼
                News API Clients
                        │
                        ▼
               Data Normalization
                        │
                        ▼
               NewsAggregatorEngine
                        │
                        ▼
               Duplicate Detection
                        │
                        ▼
                Notion Database API
                        │
                        ▼
             Structured Knowledge Base
```

---

# Project Structure

```text
newsbot_project/
│
├── clients.py
├── config.py
├── database.py
├── models.py
├── main.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## Module Breakdown

### `main.py`

The entry point of the application.

Responsible for:

- Initializing the application
- Configuring logging
- Coordinating the aggregation workflow
- Processing news articles
- Managing the overall execution

---

### `clients.py`

Contains API clients responsible for communicating with external news providers.

Responsibilities include:

- Sending HTTP requests
- Authenticating API calls
- Parsing JSON responses
- Handling request failures
- Returning standardized article data

---

### `database.py`

Manages communication with the Notion API.

Responsibilities include:

- Creating new pages
- Checking existing entries
- Uploading articles
- Managing Notion database operations

---

### `models.py`

Defines the application's data structures.

Provides standardized models for news articles, allowing all APIs to share the same internal representation.

---

### `config.py`

Stores application configuration including:

- API Keys
- Notion Token
- Database ID
- Environment variables

This keeps sensitive information separate from the source code.

---

## Workflow

```text
Start Application
        │
        ▼
Load Configuration
        │
        ▼
Initialize News Clients
        │
        ▼
Fetch Articles
        │
        ▼
Normalize Data
        │
        ▼
Check for Duplicates
        │
        ▼
Store in Notion
        │
        ▼
Log Results
```

---

## Technologies Used

### Programming Language

- Python 3.11

### APIs

- GNews API
- MediaStack API
- Currents API
- Notion API

### Libraries

- requests
- python-dotenv
- notion-client

### Development Tools

- Git
- GitHub
- Visual Studio Code

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Reaperjayjay/newsbot-project.git
```

Navigate into the project:

```bash
cd newsbot_project
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment:

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file in the project root.

Example:

```env
NOTION_TOKEN=your_notion_token
DATABASE_ID=your_database_id

GNEWS_API_KEY=your_gnews_api_key
MEDIASTACK_API_KEY=your_mediastack_api_key
CURRENTS_API_KEY=your_currents_api_key
```

---

## Running the Application

Execute:

```bash
python main.py
```

The application will:

1. Connect to all configured news providers.
2. Retrieve the latest articles.
3. Normalize article data.
4. Remove duplicates.
5. Upload new articles into the configured Notion database.
6. Generate execution logs.

---

## Skills Demonstrated

This project demonstrates experience with:

### Backend Development

- Python
- Modular application architecture
- Object-oriented programming
- Type annotations
- Exception handling

### API Integration

- REST APIs
- JSON parsing
- Authentication using API keys
- HTTP request handling
- Response validation

### Automation

- News aggregation
- Workflow automation
- Data synchronization
- Logging
- Duplicate detection

### Database Integration

- Notion API
- CRUD operations
- Structured data storage

### Software Engineering

- Separation of concerns
- Configuration management
- Modular design
- Version control with Git
- Maintainable project structure

---

## Future Improvements

Potential enhancements include:

- AI-powered article summarization
- Automatic category classification
- Sentiment analysis
- Keyword extraction
- Background scheduling
- Email digest generation
- Web dashboard
- Docker containerization
- Unit testing
- CI/CD pipeline with GitHub Actions

---

## License

This project is licensed under the MIT License.

---

## Author

**Emmanuel Chukwudi**

Aspiring AI Engineer and Backend Developer passionate about building intelligent automation tools, scalable backend systems, and AI-powered applications using Python.
