from fastapi import FastAPI
from app.api.v1 import weather_router
from app.middleware.cors import add_cors_middleware
from app.middleware.logger import add_logging_middleware
from app.middleware.error_handler import add_error_handler_middleware 
from app.middleware.gzip import add_gzip_middleware
from app.middleware.rate_limit import add_rate_limit_middleware
from app.middleware.timeout import add_timeout_middleware
from app.config.settings import get_settings
from app.utils.logger_config import setup_logger

# Load application settings
settings = get_settings()

# Initialize FastAPI application
app = FastAPI(
    title="Weather API",
    debug=settings.environment == "development"  # Enable debug mode in development
)

# Configure logger for main application
logger = setup_logger("main")

# Apply middleware in specific order
add_error_handler_middleware(app)  # Handle errors first
add_timeout_middleware(app)        # Enforce request timeouts
add_rate_limit_middleware(app)     # Apply rate limiting
add_gzip_middleware(app)          # Enable response compression
add_logging_middleware(app)       # Log requests and responses
add_cors_middleware(app)          # Add CORS support

# Register weather routes with prefix
app.include_router(weather_router.router, prefix="/api/v1")

@app.get("/")
async def health_check():
    """Check API health status asynchronously."""
    # Log health check request
    logger.info("Health check requested")
    # Return health status
    return {
        "status": "healthy",
        "environment": settings.environment,
        "message": "Weather API is running"
    }

@app.on_event("startup")
async def startup_event():
    # Log application startup
    logger.info("Weather API starting up")

@app.on_event("shutdown")
async def shutdown_event():
    # Log application shutdown
    logger.info("Weather API shutting down")


app = FastAPI()
