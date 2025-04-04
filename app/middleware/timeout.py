from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import asyncio
from app.utils.logger_config import setup_logger

class TimeoutMiddleware(BaseHTTPMiddleware):
    """Middleware to apply request time limits."""
    def __init__(self, app, timeout_seconds=10):
        super().__init__(app)
        self.timeout_seconds = timeout_seconds  # Timeout duration in seconds
        # Initialize logger for timeout events
        self.logger = setup_logger("timeout")

    async def dispatch(self, request: Request, call_next):
        try:
            # Execute request with timeout constraint
            response = await asyncio.wait_for(
                call_next(request),
                timeout=self.timeout_seconds
            )
            return response
        except asyncio.TimeoutError:
            # Log timeout occurrence
            self.logger.error(f"Request timeout after {self.timeout_seconds}s: {request.url}")
            # Raise timeout exception
            raise HTTPException(
                status_code=504,
                detail="Request Timeout"
            )

def add_timeout_middleware(app):
    """Add timeout middleware with the application."""
    app.add_middleware(TimeoutMiddleware)