from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.logger_config import setup_logger
import time

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging request and response information."""
    def __init__(self, app):
        super().__init__(app)
        # Initialize logger for HTTP events
        self.logger = setup_logger("http_logger")

    async def dispatch(self, request: Request, call_next):
        # Record start time
        start_time = time.time()
        
        # Log incoming request details
        self.logger.info(
            f"Incoming request: {request.method} {request.url} "
            f"from {request.client.host}"
        )
        
        # Execute request processing
        response = await call_next(request)
        
        # Compute request duration
        duration = time.time() - start_time
        
        # Log response details
        self.logger.info(
            f"Completed request: {request.method} {request.url} "
            f"status={response.status_code} duration={duration:.3f}s"
        )
        
        return response

def add_logging_middleware(app):
    """Register logging middleware with the application."""
    app.add_middleware(LoggingMiddleware)