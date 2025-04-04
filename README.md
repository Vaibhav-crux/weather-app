# Weather Dashboard Project

This project consists of a FastAPI backend providing weather data and a Streamlit frontend for a user-friendly weather dashboard. It’s containerized using Docker and orchestrated with Docker Compose.

## Project Structure
```
weather-app/
├── .env                  # Environment variables (not tracked in git)
├── .env.example          # Provided the dummy of .env file
├── .gitignore            # Git ignore rules
├── docker-compose.yml    # Docker Compose configuration
├── Dockerfile.backend    # Dockerfile for FastAPI backend
├── Dockerfile.frontend   # Dockerfile for Streamlit frontend
├── README.md             # Readme file
├── requirements.txt      # Requirements files
├── app/                  # FastAPI backend application
│   ├── main.py           # Entry point for the FastAPI app
│   ├── api/              # API routes
│   │   └── v1/
│   │       └── weather_router.py  # Weather API endpoint
│   ├── config/           # Configuration settings
│   │   └── settings.py   # Environment variable handling
│   ├── middleware/       # FastAPI middleware
│   │   ├── cors.py       # CORS handling
│   │   ├── error_handler.py  # Error handling
│   │   ├── gzip.py       # Response compression
│   │   ├── logger.py     # Request logging
│   │   ├── rate_limit.py # Rate limiting
│   │   └── timeout.py    # Request timeout
│   ├── schemas/          # Data models
│   │   └── weather.py    # Weather request/response schemas
│   ├── services/         # Business logic
│   │   └── v1/
│   │       └── weather_service.py  # Weather data fetching
│   └── utils/            # Utility functions
│       └── logger_config.py  # Logging configuration
└── streamlit_frontend/   # Streamlit frontend application
    ├── app.py            # Entry point for the Streamlit app
    ├── styles.css        # Custom CSS styling
    ├── components/       # UI components
    │   └── weather_display.py  # Weather data display logic
    └── utils/            # Utility functions
        └── api_client.py # API client for backend communication
```

## Overview
- **Backend**: A FastAPI application that provides a `/getCurrentWeather` endpoint to fetch current weather data for a given city, supporting JSON and XML responses. It includes middleware for CORS, logging, error handling, GZIP compression, rate limiting, and timeouts.
- **Frontend**: A Streamlit application offering an interactive dashboard to input a city name and display its weather data fetched from the backend.
- **Containerization**: Both apps are containerized with Docker and run together via Docker Compose.

## Prerequisites
- Docker and Docker Compose installed ([Docker Desktop](https://www.docker.com/products/docker-desktop) recommended for Windows).
- Python 3.11+ (optional, for local development without Docker).

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Vaibhav-crux/weather-app.git
cd weather-app
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory with the following content:
```plaintext
API_KEY=<your-rapidapi-key>
ENVIRONMENT=development
PORT=8000
WEATHER_API_URL=http://localhost:8000/api/v1/getCurrentWeather
```
- Replace `<your-rapidapi-key>` with your RapidAPI key.

### 3. Build and Run with Docker Compose
```bash
docker-compose up --build
```
- This builds and starts both the backend (FastAPI) and frontend (Streamlit) containers.
- Access:
  - Backend: `http://localhost:8000/health`
  - Frontend: `http://localhost:8501`

### 4. Stop the Application
```bash
docker-compose down
```
- Add `-v` to remove volumes: `docker-compose down -v`.

## Local Development
If you prefer running without Docker:

### Backend
1. Navigate to the backend directory:
   ```bash
   cd app
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the FastAPI app:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

### Frontend
1. Navigate to the frontend directory:
   ```bash
   cd streamlit_frontend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Usage
1. Open `http://localhost:8501` in your browser.
2. Enter a city name (e.g., "Bengaluru") in the "City Name" field.
3. Click "Get Weather" to see the current temperature, latitude, longitude, and city name.

## API Examples

### JSON Response
- **Request**:
  ```json
  {
      "city": "Bengaluru",
      "output_format": "json"
  }
  ```
- **Response**:
  ```json
  {
      "Weather": "23.1 C",
      "Latitude": "12.9833",
      "Longitude": "77.5833",
      "City": "Bengaluru"
  }
  ```

### XML Response
- **Request**:
  ```json
  {
      "city": "Bengaluru",
      "output_format": "xml"
  }
  ```
- **Response**:
  ```xml
  <root>
      <Temperature>23.1</Temperature>
      <City>Bengaluru</City>
      <Latitude>12.9833</Latitude>
      <Longitude>77.5833</Longitude>
  </root>
  ```

## Features
- **Backend**:
  - Weather data fetched from RapidAPI’s WeatherAPI.
  - Supports JSON and XML response formats.
  - Logging to `logs/weather_api.log`.
  - Rate limiting (100 requests/minute per IP).
  - Request timeout (10 seconds).
- **Frontend**:
  - Clean, styled UI with temperature-based weather icons.
  - Real-time weather updates with timestamp.