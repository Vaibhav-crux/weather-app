from starlette.middleware.gzip import GZipMiddleware
from app.utils.logger_config import setup_logger

class CustomGZipMiddleware(GZipMiddleware):
    """GZIP middleware with added logging functionality."""
    def __init__(self, app, minimum_size=1000):
        super().__init__(app, minimum_size=minimum_size)
        # Set up logger for GZIP operations
        self.logger = setup_logger("gzip")

    async def dispatch(self, request, call_next):
        # Process request and get response
        response = await call_next(request)
        # Log if response is compressed
        if response.headers.get("Content-Encoding") == "gzip":
            self.logger.debug(f"Compressed response for {request.url}")
        return response

def add_gzip_middleware(app):
    """Register GZIP middleware with the application."""
    app.add_middleware(CustomGZipMiddleware)