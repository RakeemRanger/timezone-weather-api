# Timezone Weather API

A production-ready FastAPI application that provides current time information for major timezones worldwide and weather data through OpenWeatherMap API integration.

## Features

- 🌍 Get current time for all major world timezones
- 🌤️ Fetch real-time weather data for any city
- 🔄 Combined endpoint for both timezone and weather information
- 🛡️ Comprehensive error handling with proper HTTP status codes
- 🌐 CORS middleware enabled for cross-origin requests
- 📝 Auto-generated API documentation (Swagger/ReDoc)
- ⚙️ Environment-based configuration
- ✅ Input validation with Pydantic

## Prerequisites

- Python 3.9+
- OpenWeatherMap API Key (free tier available at https://openweathermap.org/api)

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
# Edit .env and add your OpenWeatherMap API key
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
Returns application health status.

### Get All Timezones
```
GET /api/timezones
```
Returns current time for all major world timezones.

**Response Example:**
```json
{
  "timezones": [
    {
      "timezone": "America/New_York",
      "current_time": "2024-01-15T14:30:00-05:00",
      "utc_offset": "-05:00"
    }
  ]
}
```

### Get Weather Information
```
GET /api/weather?city=London&units=metric
```

**Query Parameters:**
- `city` (required): City name
- `units` (optional): Units of measurement (metric/imperial/standard, default: metric)

**Response Example:**
```json
{
  "city": "London",
  "country": "GB",
  "temperature": 15.5,
  "feels_like": 14.2,
  "humidity": 72,
  "description": "partly cloudy",
  "wind_speed": 5.5,
  "units": "metric"
}
```

### Get Combined Data
```
GET /api/combined?city=Tokyo
```

**Query Parameters:**
- `city` (required): City name
- `units` (optional): Units of measurement for weather data

**Response Example:**
```json
{
  "timezones": [...],
  "weather": {...}
}
```

## Major Timezones Supported

- America/New_York (EST/EDT)
- America/Chicago (CST/CDT)
- America/Denver (MST/MDT)
- America/Los_Angeles (PST/PDT)
- Europe/London (GMT/BST)
- Europe/Paris (CET/CEST)
- Asia/Tokyo (JST)
- Asia/Shanghai (CST)
- Asia/Dubai (GST)
- Australia/Sydney (AEST/AEDT)
- Pacific/Auckland (NZST/NZDT)

## Error Handling

The API uses standard HTTP status codes:
- `200 OK`: Successful request
- `400 Bad Request`: Invalid parameters
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error
- `503 Service Unavailable`: External service unavailable

## Environment Variables

See `.env.example` for all available configuration options.

## Testing

```bash
pytest tests/ -v
```

## License

MIT

## Contributing

Pull requests are welcome. For major changes, please open an issue first.