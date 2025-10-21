# Timezone Weather API

A production-ready FastAPI application that combines timezone information with weather data, featuring witty weather messages, 5-day forecasts, caching, and comprehensive error handling.

## Features

- 🌍 Timezone information for any location
- 🌤️ Current weather data with humorous messages
- 📅 5-day weather forecast with witty commentary
- 💬 Context-aware weather jokes and messages
- 🔄 Redis caching for improved performance
- 🛡️ Rate limiting to prevent API abuse
- 🔐 CORS support for web applications
- 📝 Comprehensive logging and monitoring
- ✅ Input validation with Pydantic
- 🧪 Unit and integration tests
- 📚 Auto-generated OpenAPI documentation

## Weather Message Examples

- **Rainy**: "You'll regret not wearing a coat!" or "Pack an umbrella unless you enjoy looking like a drowned rat"
- **Sunny**: "Time to blind everyone with your pale legs!" or "Don't forget sunscreen unless you want to look like a lobster"
- **Cloudy**: "Perfect weather for brooding dramatically" or "Nature's soft lighting - Instagram ready!"
- **Snow**: "Winter wonderland or frozen nightmare? You decide!" or "Time to build a snowman or stay inside forever"
- **Hot**: "It's so hot, eggs are frying on the sidewalk" or "Sweat is just your body crying"
- **Cold**: "Colder than your ex's heart" or "All the layers! ALL OF THEM!"
- **Windy**: "Bad hair day guaranteed" or "Your umbrella doesn't stand a chance"
- **Thunderstorm**: "Thor is angry today" or "Maybe stay inside and catch up on Netflix?"

## Prerequisites

- Python 3.9+
- Redis Server
- OpenWeatherMap API Key (get free key at https://openweathermap.org/api)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd timezone-weather-api
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your OpenWeatherMap API key
```

5. Start Redis (using Docker):
```bash
docker run -d -p 6379:6379 redis:alpine
```

## Running the Application

### Development
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

## API Endpoints

### Health Check
```
GET /health
```

Returns API health status and Redis connection status.

### Get Timezone Information
```
GET /api/v1/timezone/{timezone}
```

Get timezone information for a specific timezone.

**Path Parameters:**
- `timezone`: Timezone name (e.g., "America/New_York", "Europe/London")

**Example:**
```bash
curl http://localhost:8000/api/v1/timezone/America/New_York
```

**Response:**
```json
{
  "timezone": "America/New_York",
  "current_time": "2024-01-15T10:30:00-05:00",
  "utc_offset": "-05:00",
  "is_dst": false,
  "abbreviation": "EST"
}
```

### Get Current Weather
```
GET /api/v1/weather/current
```

Get current weather data with a witty message for a specific location.

**Query Parameters:**
- `city`: City name (required)
- `country_code`: ISO 3166 country code (optional, e.g., "US", "GB")
- `units`: Temperature units - "metric" (Celsius) or "imperial" (Fahrenheit), default: "metric"

**Example:**
```bash
curl "http://localhost:8000/api/v1/weather/current?city=London&country_code=GB&units=metric"
```

**Response:**
```json
{
  "location": "London, GB",
  "temperature": 12.5,
  "feels_like": 10.2,
  "humidity": 76,
  "description": "light rain",
  "condition": "Rain",
  "wind_speed": 5.5,
  "timestamp": "2024-01-15T15:30:00Z",
  "units": "metric",
  "witty_message": "You'll regret not wearing a coat!"
}
```

### Get 5-Day Weather Forecast
```
GET /api/v1/weather/forecast
```

Get 5-day weather forecast with witty messages for each day.

**Query Parameters:**
- `city`: City name (required)
- `country_code`: ISO 3166 country code (optional)
- `units`: Temperature units - "metric" or "imperial", default: "metric"

**Example:**
```bash
curl "http://localhost:8000/api/v1/weather/forecast?city=New%20York&country_code=US&units=imperial"
```

**Response:**
```json
{
  "location": "New York, US",
  "units": "imperial",
  "forecast": [
    {
      "date": "2024-01-15",
      "temperature": {
        "min": 32.5,
        "max": 45.2,
        "avg": 38.8
      },
      "description": "clear sky",
      "condition": "Clear",
      "humidity": 65,
      "wind_speed": 8.5,
      "witty_message": "Time to blind everyone with your pale legs!"
    },
    {
      "date": "2024-01-16",
      "temperature": {
        "min": 28.3,
        "max": 38.7,
        "avg": 33.5
      },
      "description": "light snow",
      "condition": "Snow",
      "humidity": 78,
      "wind_speed": 12.3,
      "witty_message": "Winter wonderland or frozen nightmare? You decide!"
    }
  ]
}
```

### Combined Timezone and Weather
```
GET /api/v1/timezone-weather
```

Get both timezone information and current weather for a location.

**Query Parameters:**
- `city`: City name (required)
- `timezone`: Timezone name (required)
- `country_code`: ISO 3166 country code (optional)
- `units`: Temperature units, default: "metric"

**Example:**
```bash
curl "http://localhost:8000/api/v1/timezone-weather?city=Tokyo&timezone=Asia/Tokyo&country_code=JP"
```

**Response:**
```json
{
  "timezone": {
    "timezone": "Asia/Tokyo",
    "current_time": "2024-01-16T00:30:00+09:00",
    "utc_offset": "+09:00",
    "is_dst": false,
    "abbreviation": "JST"
  },
  "weather": {
    "location": "Tokyo, JP",
    "temperature": 8.5,
    "feels_like": 6.2,
    "humidity": 62,
    "description": "few clouds",
    "condition": "Clouds",
    "wind_speed": 3.5,
    "timestamp": "2024-01-15T15:30:00Z",
    "units": "metric",
    "witty_message": "Perfect weather for brooding dramatically"
  }
}
```

## Weather Conditions

The API recognizes the following weather conditions and provides appropriate witty messages:

- **Rain**: Rainy weather messages
- **Clear**: Sunny weather messages
- **Clouds**: Cloudy weather messages
- **Snow**: Snow weather messages
- **Thunderstorm**: Thunderstorm messages
- **Drizzle**: Light rain messages
- **Mist/Fog/Haze**: Cloudy weather messages

Additional modifiers based on temperature:
- **Hot** (>30°C / 86°F): Hot weather messages
- **Cold** (<5°C / 41°F): Cold weather messages

Additional modifiers based on wind:
- **Windy** (>10 m/s): Windy weather messages

## Testing

Run tests:
```bash
pytest
```

With coverage:
```bash
pytest --cov=app --cov-report=html
```

Run specific test file:
```bash
pytest tests/api/test_weather.py -v
```

## Code Quality

Format code:
```bash
black app/
isort app/
```

Lint:
```bash
flake8 app/
mypy app/
```

Run pre-commit hooks:
```bash
pre-commit run --all-files
```

## Docker Deployment

Build image:
```bash
docker build -t timezone-weather-api .
```

Run with docker-compose:
```bash
docker-compose up -d
```

## Environment Variables

See `.env.example` for all available configuration options.

### Required Variables
- `WEATHER_API_KEY`: Your OpenWeatherMap API key

### Optional Variables
- `REDIS_HOST`: Redis host (default: localhost)
- `REDIS_PORT`: Redis port (default: 6379)
- `CACHE_TTL`: Cache time-to-live in seconds (default: 1800)
- `RATE_LIMIT_PER_MINUTE`: Rate limit per minute (default: 60)
- `LOG_LEVEL`: Logging level (default: INFO)

## Architecture

```
timezone-weather-api/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── timezone.py      # Timezone endpoints
│   │       ├── weather.py       # Weather endpoints
│   │       └── combined.py      # Combined endpoints
│   ├── core/
│   │   ├── config.py            # Configuration settings
│   │   └── logging_config.py    # Logging configuration
│   ├── models/                  # Database models (if needed)
│   ├── schemas/
│   │   ├── timezone.py          # Timezone schemas
│   │   └── weather.py           # Weather schemas
│   ├── services/
│   │   ├── cache.py             # Redis cache service
│   │   ├── timezone_service.py  # Timezone logic
│   │   ├── weather_client.py    # Weather API client
│   │   └── weather_messages.py  # Witty message generator
│   ├── utils/                   # Utility functions
│   └── main.py                  # FastAPI application
├── tests/                       # Test suite
├── .env.example                 # Environment variables template
├── requirements.txt             # Production dependencies
├── Dockerfile                   # Docker configuration
└── docker-compose.yml           # Docker Compose configuration
```

## Popular City Examples

Try these popular cities:
- New York, US (America/New_York)
- London, GB (Europe/London)
- Tokyo, JP (Asia/Tokyo)
- Sydney, AU (Australia/Sydney)
- Paris, FR (Europe/Paris)
- Dubai, AE (Asia/Dubai)
- Singapore, SG (Asia/Singapore)

## License

MIT

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Support

For issues and questions, please open an issue on GitHub.