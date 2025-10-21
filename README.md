# Timezone Weather API

A FastAPI-based REST API that provides timezone information and weather data for locations worldwide.

## Features

- Get timezone information for any location
- Fetch current weather data
- Combined endpoint for timezone and weather in a single request
- Caching for improved performance
- Comprehensive error handling
- Docker support for easy deployment

## Requirements

- Python 3.9+
- Docker (optional)
- OpenWeatherMap API key (for weather endpoints)

## Installation

### Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd timezone-weather-api
```

2. Create a virtual environment:
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
export OPENWEATHER_API_KEY=your_api_key_here
```

5. Run the application:
```bash
uvicorn app.main:app --reload
```

### Docker Deployment

1. Build and run with Docker Compose:
```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Usage Examples

### 1. Get Timezone Information

Retrieve timezone information for a specific location.

**Endpoint:** `GET /api/v1/timezone`

**Parameters:**
- `location` (required): City name, coordinates, or address

**Example Request:**
```bash
curl "http://localhost:8000/api/v1/timezone?location=New%20York"
```

**Example Response:**
```json
{
  "location": "New York",
  "timezone": "America/New_York",
  "utc_offset": "-05:00",
  "current_time": "2024-01-15T14:30:00-05:00",
  "is_dst": false,
  "coordinates": {
    "latitude": 40.7128,
    "longitude": -74.0060
  }
}
```

**Another Example with Coordinates:**
```bash
curl "http://localhost:8000/api/v1/timezone?location=51.5074,-0.1278"
```

**Response:**
```json
{
  "location": "51.5074,-0.1278",
  "timezone": "Europe/London",
  "utc_offset": "+00:00",
  "current_time": "2024-01-15T19:30:00+00:00",
  "is_dst": false,
  "coordinates": {
    "latitude": 51.5074,
    "longitude": -0.1278
  }
}
```

### 2. Get Weather Information

Retrieve current weather data for a location.

**Endpoint:** `GET /api/v1/weather`

**Parameters:**
- `location` (required): City name or coordinates
- `units` (optional): `metric` (default), `imperial`, or `standard`

**Example Request (Metric):**
```bash
curl "http://localhost:8000/api/v1/weather?location=London&units=metric"
```

**Example Response:**
```json
{
  "location": "London",
  "coordinates": {
    "latitude": 51.5074,
    "longitude": -0.1278
  },
  "temperature": {
    "current": 12.5,
    "feels_like": 11.2,
    "min": 10.0,
    "max": 14.0,
    "unit": "celsius"
  },
  "conditions": {
    "main": "Clouds",
    "description": "overcast clouds",
    "icon": "04d"
  },
  "humidity": 75,
  "pressure": 1013,
  "wind": {
    "speed": 5.2,
    "direction": 230,
    "unit": "m/s"
  },
  "visibility": 10000,
  "timestamp": "2024-01-15T19:30:00Z"
}
```

**Example Request (Imperial):**
```bash
curl "http://localhost:8000/api/v1/weather?location=Los%20Angeles&units=imperial"
```

**Response:**
```json
{
  "location": "Los Angeles",
  "coordinates": {
    "latitude": 34.0522,
    "longitude": -118.2437
  },
  "temperature": {
    "current": 68.5,
    "feels_like": 67.8,
    "min": 65.0,
    "max": 72.0,
    "unit": "fahrenheit"
  },
  "conditions": {
    "main": "Clear",
    "description": "clear sky",
    "icon": "01d"
  },
  "humidity": 45,
  "pressure": 1015,
  "wind": {
    "speed": 8.5,
    "direction": 270,
    "unit": "mph"
  },
  "visibility": 10000,
  "timestamp": "2024-01-15T11:30:00Z"
}
```

### 3. Get Combined Timezone and Weather Information

Retrieve both timezone and weather data in a single request.

**Endpoint:** `GET /api/v1/combined`

**Parameters:**
- `location` (required): City name or coordinates
- `units` (optional): `metric` (default), `imperial`, or `standard`

**Example Request:**
```bash
curl "http://localhost:8000/api/v1/combined?location=Tokyo&units=metric"
```

**Example Response:**
```json
{
  "location": "Tokyo",
  "timezone": {
    "timezone": "Asia/Tokyo",
    "utc_offset": "+09:00",
    "current_time": "2024-01-16T04:30:00+09:00",
    "is_dst": false,
    "coordinates": {
      "latitude": 35.6762,
      "longitude": 139.6503
    }
  },
  "weather": {
    "coordinates": {
      "latitude": 35.6762,
      "longitude": 139.6503
    },
    "temperature": {
      "current": 8.5,
      "feels_like": 6.2,
      "min": 6.0,
      "max": 10.0,
      "unit": "celsius"
    },
    "conditions": {
      "main": "Clear",
      "description": "clear sky",
      "icon": "01n"
    },
    "humidity": 55,
    "pressure": 1020,
    "wind": {
      "speed": 3.5,
      "direction": 180,
      "unit": "m/s"
    },
    "visibility": 10000,
    "timestamp": "2024-01-15T19:30:00Z"
  },
  "local_time": "2024-01-16T04:30:00+09:00"
}
```

### 4. Health Check

Check if the API is running.

**Endpoint:** `GET /health`

**Example Request:**
```bash
curl "http://localhost:8000/health"
```

**Example Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T19:30:00Z"
}
```

### Error Responses

The API returns structured error responses:

**Example - Invalid Location:**
```bash
curl "http://localhost:8000/api/v1/timezone?location=InvalidLocationXYZ123"
```

**Response (404):**
```json
{
  "detail": "Location not found: InvalidLocationXYZ123"
}
```

**Example - Missing Required Parameter:**
```bash
curl "http://localhost:8000/api/v1/weather"
```

**Response (422):**
```json
{
  "detail": [
    {
      "loc": ["query", "location"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**Example - Invalid API Key:**
```bash
curl "http://localhost:8000/api/v1/weather?location=Paris"
```

**Response (500):**
```json
{
  "detail": "Weather service error: Invalid API key"
}
```

## Python Client Example

Here's how to use the API with Python's `requests` library:

```python
import requests

BASE_URL = "http://localhost:8000"

# Get timezone information
response = requests.get(f"{BASE_URL}/api/v1/timezone", params={"location": "Paris"})
timezone_data = response.json()
print(f"Timezone: {timezone_data['timezone']}")
print(f"Current time: {timezone_data['current_time']}")

# Get weather information
response = requests.get(f"{BASE_URL}/api/v1/weather", params={
    "location": "Paris",
    "units": "metric"
})
weather_data = response.json()
print(f"Temperature: {weather_data['temperature']['current']}°C")
print(f"Conditions: {weather_data['conditions']['description']}")

# Get combined information
response = requests.get(f"{BASE_URL}/api/v1/combined", params={
    "location": "Paris",
    "units": "metric"
})
combined_data = response.json()
print(f"Location: {combined_data['location']}")
print(f"Local time: {combined_data['local_time']}")
print(f"Temperature: {combined_data['weather']['temperature']['current']}°C")
```

## JavaScript/Node.js Client Example

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:8000';

async function getTimezone(location) {
  try {
    const response = await axios.get(`${BASE_URL}/api/v1/timezone`, {
      params: { location }
    });
    return response.data;
  } catch (error) {
    console.error('Error:', error.response.data);
  }
}

async function getWeather(location, units = 'metric') {
  try {
    const response = await axios.get(`${BASE_URL}/api/v1/weather`, {
      params: { location, units }
    });
    return response.data;
  } catch (error) {
    console.error('Error:', error.response.data);
  }
}

async function getCombined(location, units = 'metric') {
  try {
    const response = await axios.get(`${BASE_URL}/api/v1/combined`, {
      params: { location, units }
    });
    return response.data;
  } catch (error) {
    console.error('Error:', error.response.data);
  }
}

// Usage
(async () => {
  const timezone = await getTimezone('Berlin');
  console.log('Timezone:', timezone.timezone);
  
  const weather = await getWeather('Berlin', 'metric');
  console.log('Temperature:', weather.temperature.current);
  
  const combined = await getCombined('Berlin');
  console.log('Local time:', combined.local_time);
})();
```

## Rate Limiting & Caching

The API implements caching to reduce external API calls and improve response times:
- Timezone data is cached for 24 hours
- Weather data is cached for 10 minutes
- Cache is stored in-memory (Redis support can be added)

## Development

### Running Tests

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/api/test_weather.py
```

### Code Style

The project uses:
- Black for code formatting
- Flake8 for linting
- MyPy for type checking

```bash
black app/
flake8 app/
mypy app/
```

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|----------|
| `OPENWEATHER_API_KEY` | OpenWeatherMap API key | Yes | - |
| `CACHE_TTL_TIMEZONE` | Timezone cache TTL (seconds) | No | 86400 |
| `CACHE_TTL_WEATHER` | Weather cache TTL (seconds) | No | 600 |
| `LOG_LEVEL` | Logging level | No | INFO |

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
