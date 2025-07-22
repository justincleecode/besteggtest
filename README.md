# NYTimes Article Microservice

A FastAPI-based microservice that integrates with the New York Times Developer APIs to retrieve and expose article data.

## Features

- **Top Stories Endpoint**: Retrieves the two most recent top stories from arts, food, movies, travel, and science categories
- **Article Search Endpoint**: Searches NYTimes articles with keyword and date filtering
- **Auto-generated OpenAPI/Swagger Documentation**: Available at `/docs`
- **Comprehensive Unit Tests**: Covers both success and error scenarios
- **Pydantic Models**: For request/response validation
- **Error Handling**: Proper HTTP status codes and error messages

## Prerequisites

1. **NYTimes Developer API Key**: Register at [NYTimes Developer Portal](https://developer.nytimes.com/get-started)
2. **Python 3.8+**
3. **Git** (for cloning the repository)

## Setup Instructions

### Step 1: Clone and Navigate to Project
```bash
git clone <repository-url>
cd bestegg
```

### Step 2: Create Virtual Environment

**On Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### Step 3: Install Dependencies
With the virtual environment activated:
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
   
2. Edit `.env` file and replace `your_api_key_here` with your actual NYTimes API key:
   ```
   NYTIMES_API_KEY=your_actual_nytimes_api_key_here
   ```

### Step 5: Run the Application

**Method 1: Using the run script (Recommended)**
```bash
python run.py
```

**Method 2: Using uvicorn directly**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 6: Verify Installation
Once the server is running, you can:
- Visit http://localhost:8000 for the API root
- Visit http://localhost:8000/docs for interactive Swagger documentation
- Visit http://localhost:8000/redoc for ReDoc documentation

## API Endpoints

### GET `/`
Root endpoint with API information and available endpoints.

### GET `/nytimes/topstories`
Returns the two most recent top stories from each category (arts, food, movies, travel, science).

**Response Format**:
```json
{
  "stories": [
    {
      "title": "Article Title",
      "section": "arts",
      "url": "https://nytimes.com/article-url",
      "abstract": "Article abstract...",
      "published_date": "2024-01-01T10:00:00-05:00"
    }
  ],
  "total_count": 10
}
```

### GET `/nytimes/articlesearch`
Searches NYTimes articles using keywords and optional date filters.

**Query Parameters**:
- `q` (required): Search keyword
- `begin_date` (optional): Start date in YYYYMMDD format
- `end_date` (optional): End date in YYYYMMDD format

**Example**: `/nytimes/articlesearch?q=technology&begin_date=20240101&end_date=20240131`

**Response Format**:
```json
{
  "articles": [
    {
      "headline": "Article Headline",
      "snippet": "Article snippet...",
      "web_url": "https://nytimes.com/article-url",
      "pub_date": "2024-01-01T10:00:00+0000"
    }
  ],
  "total_count": 5,
  "query": "technology"
}
```

## Development Workflow

### Daily Development
1. **Activate virtual environment** (do this every time you work on the project):
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

2. **Run the development server**:
   ```bash
   python run.py
   ```
   The server will auto-reload when you make changes to the code.

3. **Deactivate virtual environment** when done:
   ```bash
   deactivate
   ```

### Adding New Dependencies
1. Activate virtual environment
2. Install the package: `pip install package-name`
3. Update requirements: `pip freeze > requirements.txt`

## Testing

### Running Tests
With virtual environment activated:
```bash
pytest tests/ -v
```

### Running Specific Tests
```bash
# Run tests for a specific class
pytest tests/test_nytimes.py::TestTopStoriesEndpoint -v

# Run a specific test method
pytest tests/test_nytimes.py::TestTopStoriesEndpoint::test_get_top_stories_success -v
```

### Test Coverage
The tests cover:
- Root endpoint functionality
- Top stories endpoint (success and error cases)
- Article search endpoint (success, validation, and error cases)
- Date filtering functionality
- API error handling
- Mock external API calls for reliable testing

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application setup
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py    # Configuration settings
│   ├── models/
│   │   ├── __init__.py
│   │   └── nytimes.py   # Pydantic models
│   └── routers/
│       ├── __init__.py
│       └── nytimes.py   # NYTimes API endpoints
├── tests/
│   ├── __init__.py
│   └── test_nytimes.py  # Unit tests
├── run.py               # Application entry point
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
└── README.md           # This file
```

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **httpx**: Async HTTP client for API requests
- **pytest**: Testing framework
- **uvicorn**: ASGI server for running the application
- **python-dotenv**: Environment variable management
- **pydantic-settings**: Configuration management

## Troubleshooting

### Common Issues

**1. Virtual Environment Issues**
```bash
# If you get "venv is not recognized" on Windows:
python -m venv venv

# If you get permission errors on macOS/Linux:
sudo python3 -m venv venv
```

**2. API Key Issues**
```bash
# Error: "NYTIMES_API_KEY environment variable is required"
# Solution: Make sure .env file exists and contains your API key
cp .env.example .env
# Then edit .env and add your actual API key
```

**3. Import Errors**
```bash
# Error: "ModuleNotFoundError: No module named 'app'"
# Solution: Make sure you're in the project root directory and virtual environment is activated
cd /path/to/bestegg
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

**4. Port Already in Use**
```bash
# Error: "Address already in use"
# Solution: Kill the process using port 8000 or use a different port
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:8000 | xargs kill -9
```

**5. NYTimes API Errors**
- **401 Unauthorized**: Check your API key is correct
- **429 Too Many Requests**: You've hit the rate limit, wait and try again
- **403 Forbidden**: Your API key may not have access to the requested endpoint

### Getting Help
- Check the FastAPI documentation: https://fastapi.tiangolo.com/
- NYTimes API documentation: https://developer.nytimes.com/docs
- Check server logs for detailed error messages

## Error Handling

The microservice includes comprehensive error handling:
- HTTP 422 for validation errors (missing required parameters)
- HTTP 500 for external API errors or unexpected issues
- Detailed error messages for debugging

## Development Notes

- The application uses async/await for non-blocking API calls
- CORS middleware is enabled for cross-origin requests
- Environment variables are used for secure API key management
- Comprehensive logging and error messages for troubleshooting
- Virtual environment isolation ensures consistent dependencies
